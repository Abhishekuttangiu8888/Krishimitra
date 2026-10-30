import requests
from pprint import pprint

BASE_URL = "https://api.agmarknet.gov.in/v1"

session = requests.Session()

session.headers.update({
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://agmarknet.gov.in",
    "Referer": "https://agmarknet.gov.in/",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/135.0.0.0 Safari/537.36"
    ),
})

STATE_ID = 16
MARKET_ID = 108  # APMC Hubballi

crops = {
    "Paddy (Common)": 2,
    "Maize": 4,
    "Ragi": 30,
    "Onion": 23,
    "Tomato": 65,
}

endpoints = {
    "Commodity price last week":
        "/prices-and-arrivals/commodity-price/lastweek",
    "Market price last week":
        "/prices-and-arrivals/market-price/lastweek",
}

for crop_name, commodity_id in crops.items():
    print("\n" + "=" * 55)
    print("CROP:", crop_name)
    print("=" * 55)

    params = {
        "marketId": MARKET_ID,
        "stateId": STATE_ID,
        "commodityId": commodity_id,
    }

    for title, path in endpoints.items():
        print(f"\n{title}")

        try:
            response = session.get(
                BASE_URL + path,
                params=params,
                timeout=(5, 15),
            )

            print("HTTP Status:", response.status_code)

            try:
                data = response.json()
                pprint(data)
            except ValueError:
                print(response.text[:1000])

        except requests.RequestException as error:
            print("Request error:", error)