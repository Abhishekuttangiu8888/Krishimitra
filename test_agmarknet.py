
import os
import requests
from dotenv import load_dotenv

# Load API key from the existing .env file
load_dotenv()

API_KEY = os.getenv("AGMARKNET_API_KEY")

URL = (
    "https://api.data.gov.in/resource/"
    "9ef84268-d588-465a-a308-a864a43d0070"
)


def test_api():
    if not API_KEY:
        print("ERROR: AGMARKNET_API_KEY not found in .env")
        return

    params = {
        "format": "json",
        "limit": 5,
    }

    headers = {
        "X-Api-Key": API_KEY,
        "Accept": "application/json",
    }

    try:
        print("Connecting to AGMARKNET API...")

        response = requests.get(
            URL,
            params=params,
            headers=headers,
            timeout=60,
        )

        print("HTTP Status:", response.status_code)

        if not response.ok:
            print("API Error:", response.text[:1000])
            return

        data = response.json()

        print("\nAPI connection successful!")
        print("Total records:", data.get("total", "Not provided"))

        records = data.get("records", [])

        if not records:
            print("No records returned.")
            print("Response:", data)
            return

        print("\nSample mandi records:\n")

        for record in records:
            print("State:", record.get("state"))
            print("District:", record.get("district"))
            print("Market:", record.get("market"))
            print("Commodity:", record.get("commodity"))
            print("Variety:", record.get("variety"))
            print("Arrival date:", record.get("arrival_date"))
            print("Minimum price:", record.get("min_price"))
            print("Maximum price:", record.get("max_price"))
            print("Modal price:", record.get("modal_price"))
            print("-" * 40)

    except requests.exceptions.Timeout:
        print("ERROR: API request timed out.")

    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the API.")

    except requests.exceptions.RequestException as error:
        print("Request error:", error)

    except ValueError:
        print("ERROR: API did not return valid JSON.")


if __name__ == "__main__":
    test_api()
