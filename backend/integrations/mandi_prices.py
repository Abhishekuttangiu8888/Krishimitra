import requests
from functools import lru_cache
from datetime import date, datetime


AGMARKNET_HOME = "https://agmarknet.gov.in/"

AGMARKNET_API_BASE = "https://api.agmarknet.gov.in/v1"

FILTERS_URL = f"{AGMARKNET_API_BASE}/daily-price-arrival/filters"

COMMODITY_PRICE_URL = (
    f"{AGMARKNET_API_BASE}/prices-and-arrivals/commodity-price/lastweek"
)

KARNATAKA_STATE_ID = 16


class MandiDataError(Exception):
    """Raised when AGMARKNET data cannot be retrieved or processed."""
    pass


def _create_session():
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

    return session


@lru_cache(maxsize=1)
def _fetch_filter_data():
    session = None

    try:
        session = _create_session()

        response = session.get(
            FILTERS_URL,
            timeout=(5, 20),
        )
        response.raise_for_status()

        payload = response.json()

        if not payload.get("status"):
            raise MandiDataError(
                "AGMARKNET filters could not be loaded."
            )

        data = payload.get("data", {})

        required_keys = [
            "state_data",
            "district_data",
            "market_data",
            "cmdt_data",
        ]

        for key in required_keys:
            if not isinstance(data.get(key), list):
                raise MandiDataError(
                    f"Invalid AGMARKNET filter data: {key}"
                )

        return data

    except MandiDataError:
        raise

    except (requests.RequestException, ValueError) as error:
        raise MandiDataError(
            "Unable to retrieve AGMARKNET filters."
        ) from error

    finally:
        if session:
            session.close()


def get_mandi_filters(refresh=False):
    if refresh:
        _fetch_filter_data.cache_clear()

    data = _fetch_filter_data()

    states = data["state_data"]
    districts = data["district_data"]
    markets = data["market_data"]
    commodities = data["cmdt_data"]

    karnataka_districts = [
        item
        for item in districts
        if item.get("state_id") == KARNATAKA_STATE_ID
    ]

    district_ids = {
        item["id"]
        for item in karnataka_districts
    }

    karnataka_markets = [
        item
        for item in markets
        if (
            item.get("state_id") == KARNATAKA_STATE_ID
            and item.get("district_id") in district_ids
        )
    ]

    return {
        "states": [
            {
                "id": item["state_id"],
                "name": item["state_name"],
            }
            for item in states
            if item.get("state_id") != 100000
        ],

        "districts": [
            {
                "id": item["id"],
                "name": item["district_name"],
                "state_id": item.get("state_id"),
            }
            for item in karnataka_districts
        ],

        "markets": [
            {
                "id": item["id"],
                "name": item["mkt_name"].strip(),
                "district_id": item.get("district_id"),
                "state_id": item.get("state_id"),
            }
            for item in karnataka_markets
        ],

        "commodities": [
            {
                "id": item["cmdt_id"],
                "name": item["cmdt_name"].strip(),
                "group_id": item.get("cmdt_group_id"),
            }
            for item in commodities
        ],
    }


def _is_numeric_price(value):
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
    )


def get_mandi_prices(
    district_id: int,
    market_id: int,
    commodity_id: int,
    date: date | None = None,
):
    """
    Fetch the last week's reported prices for a Karnataka market
    and commodity.

    Note:
    AGMARKNET's confirmed lastweek endpoint does not accept a
    selected historical date. It returns its available last-week
    data instead.
    """

    # Validate the selected market and commodity against Karnataka filters.
    filters = get_mandi_filters()

    market = next(
        (
            item for item in filters["markets"]
            if item["id"] == market_id
            and item["district_id"] == district_id
        ),
        None,
    )

    if not market:
        raise MandiDataError(
            "The selected market does not belong to this Karnataka district."
        )

    commodity = next(
        (
            item for item in filters["commodities"]
            if item["id"] == commodity_id
        ),
        None,
    )

    if not commodity:
        raise MandiDataError(
            "The selected commodity was not found."
        )

    session = None

    try:
        session = _create_session()

        params = {
            "marketId": market_id,
            "stateId": KARNATAKA_STATE_ID,
            "commodityId": commodity_id,
        }

        response = session.get(
            COMMODITY_PRICE_URL,
            params=params,
            timeout=(5, 20),
        )

        response.raise_for_status()

        payload = response.json()

        if not payload.get("success"):
            raise MandiDataError(
                payload.get("message", "AGMARKNET returned no data.")
            )

        raw_rows = payload.get("data", [])

        columns = payload.get("columns", [])

        date_columns = [
            column["key"]
            for column in columns
            if column.get("key")
            and column["key"] not in ("variety", "unitOfPrice")
        ]

        records = []

        for row in raw_rows:
            daily_prices = []

            for date_key in date_columns:
                value = row.get(date_key)

                if _is_numeric_price(value):
                    price = float(value)
                else:
                    price = None

                daily_prices.append({
                    "date": date_key,
                    "price": price,
                    "reported": price is not None,
                })

            available_prices = [
                item for item in daily_prices
                if item["price"] is not None
            ]

            latest = (
                available_prices[0]
                if available_prices
                else None
            )

            records.append({
                "variety": row.get("variety", "Unknown"),
                "unit": row.get("unitOfPrice", "NR"),
                "daily_prices": daily_prices,
                "latest_price": latest["price"] if latest else None,
                "latest_date": latest["date"] if latest else None,
                "has_report": bool(available_prices),
            })

        has_any_report = any(
            record["has_report"]
            for record in records
        )

        return {
            "source": "AGMARKNET",
            "state": "Karnataka",
            "district": next(
                item["name"]
                for item in filters["districts"]
                if item["id"] == district_id
            ),
            "market": market["name"],
            "commodity": commodity["name"],
            "market_id": market_id,
            "commodity_id": commodity_id,
            "selected_date": date.isoformat() if date else None,
            "report_period": "Last 7 days available from AGMARKNET",
            "available_dates": date_columns,
            "records": records,
            "has_report": has_any_report,
            "message": (
                "Price data fetched successfully."
                if has_any_report
                else "No reported prices are available for this selection."
            ),
        }

    except MandiDataError:
        raise

    except requests.Timeout as error:
        raise MandiDataError(
            "AGMARKNET price request timed out. Please try again."
        ) from error

    except requests.RequestException as error:
        raise MandiDataError(
            "Unable to connect to AGMARKNET price service."
        ) from error

    except ValueError as error:
        raise MandiDataError(
            "AGMARKNET returned an invalid response."
        ) from error

    finally:
        if session:
            session.close()