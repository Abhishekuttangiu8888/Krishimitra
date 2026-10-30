from backend.integrations.mandi_prices import _create_session

url = (
    "https://api.agmarknet.gov.in/v1/"
    "prices-and-arrivals/market-report/daily"
)

payload = {
    "date": "2026-10-31",
    "marketIds": [101],  # Belgaum APMC
    "stateIds": [16],    # Karnataka
    "includeExcel": False,
}

response = _create_session().post(
    url,
    json=payload,
    timeout=30,
)

print("STATUS:", response.status_code)
print("CONTENT TYPE:", response.headers.get("content-type"))
print("RESPONSE:")
print(response.text[:12000])