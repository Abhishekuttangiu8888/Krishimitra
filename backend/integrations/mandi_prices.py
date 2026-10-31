
import requests
from functools import lru_cache
from datetime import date
from typing import Optional


AGMARKNET_API_BASE = "https://api.agmarknet.gov.in/v1"

FILTERS_URL = (
    f"{AGMARKNET_API_BASE}/daily-price-arrival/filters"
)

COMMODITY_PRICE_URL = (
    f"{AGMARKNET_API_BASE}/prices-and-arrivals/commodity-price/lastweek"
)

KARNATAKA_STATE_ID = 16
REQUEST_TIMEOUT = (5, 15)


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
    session = _create_session()

    try:
        response = session.get(
            FILTERS_URL,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        payload = response.json()

        if not isinstance(payload, dict) or not payload.get("status"):
            raise MandiDataError(
                "AGMARKNET filters could not be loaded."
            )

        data = payload.get("data", {})

        required_keys = (
            "state_data",
            "district_data",
            "market_data",
            "cmdt_data",
        )

        for key in required_keys:
            if not isinstance(data.get(key), list):
                raise MandiDataError(
                    f"Invalid AGMARKNET filter data: {key}"
                )

        return data

    except MandiDataError:
        raise

    except requests.Timeout as error:
        raise MandiDataError(
            "AGMARKNET filter request timed out."
        ) from error

    except (requests.RequestException, ValueError) as error:
        raise MandiDataError(
            "Unable to retrieve AGMARKNET filters."
        ) from error

    finally:
        session.close()


@lru_cache(maxsize=1)
def _build_mandi_filters():
    data = _fetch_filter_data()

    karnataka_districts = [
        item
        for item in data["district_data"]
        if item.get("state_id") == KARNATAKA_STATE_ID
    ]

    district_ids = {
        item["id"]
        for item in karnataka_districts
        if item.get("id") is not None
    }

    karnataka_markets = [
        item
        for item in data["market_data"]
        if (
            item.get("state_id") == KARNATAKA_STATE_ID
            and item.get("district_id") in district_ids
        )
    ]

    districts = [
        {
            "id": item["id"],
            "name": item["district_name"],
            "state_id": item.get("state_id"),
        }
        for item in karnataka_districts
        if item.get("id") is not None
    ]

    markets = [
        {
            "id": item["id"],
            "name": (item.get("mkt_name") or "").strip(),
            "district_id": item.get("district_id"),
            "state_id": item.get("state_id"),
        }
        for item in karnataka_markets
        if item.get("id") is not None
    ]

    commodities = [
        {
            "id": item["cmdt_id"],
            "name": (item.get("cmdt_name") or "").strip(),
            "group_id": item.get("cmdt_group_id"),
        }
        for item in data["cmdt_data"]
        if item.get("cmdt_id") is not None
    ]

    states = [
        {
            "id": item["state_id"],
            "name": item["state_name"],
        }
        for item in data["state_data"]
        if item.get("state_id") != 100000
    ]

    return {
        "states": states,
        "districts": districts,
        "markets": markets,
        "commodities": commodities,
        "_district_lookup": {
            item["id"]: item["name"]
            for item in districts
        },
        "_market_lookup": {
            item["id"]: item
            for item in markets
        },
        "_commodity_lookup": {
            item["id"]: item
            for item in commodities
        },
    }


def get_mandi_filters(refresh=False):
    if refresh:
        _build_mandi_filters.cache_clear()
        _fetch_filter_data.cache_clear()

    cached = _build_mandi_filters()

    return {
        "states": cached["states"],
        "districts": cached["districts"],
        "markets": cached["markets"],
        "commodities": cached["commodities"],
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
    date: Optional[date] = None,
):
    filters = _build_mandi_filters()

    market = filters["_market_lookup"].get(market_id)

    if not market or market["district_id"] != district_id:
        raise MandiDataError(
            "The selected market does not belong to this Karnataka district."
        )

    commodity = filters["_commodity_lookup"].get(commodity_id)

    if not commodity:
        raise MandiDataError(
            "The selected commodity was not found."
        )

    session = _create_session()

    try:
        params = {
            "marketId": market_id,
            "stateId": KARNATAKA_STATE_ID,
            "commodityId": commodity_id,
        }

        response = session.get(
            COMMODITY_PRICE_URL,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()
        payload = response.json()

        if not isinstance(payload, dict):
            raise MandiDataError(
                "AGMARKNET returned an invalid response."
            )

        if not payload.get("success"):
            raise MandiDataError(
                payload.get("message", "AGMARKNET returned no data.")
            )

        raw_rows = payload.get("data") or []
        columns = payload.get("columns") or []

        if not isinstance(raw_rows, list) or not isinstance(columns, list):
            raise MandiDataError(
                "AGMARKNET returned an invalid price data structure."
            )

        date_columns = [
            column["key"]
            for column in columns
            if (
                isinstance(column, dict)
                and column.get("key")
                and column["key"] not in ("variety", "unitOfPrice")
            )
        ]

        records = []

        for row in raw_rows:
            if not isinstance(row, dict):
                continue

            daily_prices = []

            for date_key in date_columns:
                value = row.get(date_key)

                price = (
                    float(value)
                    if _is_numeric_price(value)
                    else None
                )

                daily_prices.append({
                    "date": date_key,
                    "price": price,
                    "reported": price is not None,
                })

            available_prices = [
                item
                for item in daily_prices
                if item["price"] is not None
            ]

            latest = available_prices[0] if available_prices else None

            records.append({
                "variety": row.get("variety") or "Unknown",
                "unit": row.get("unitOfPrice") or "NR",
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
            "district": filters["_district_lookup"][district_id],
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
        session.close()
