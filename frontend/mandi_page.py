
import requests
import streamlit as st
import pandas as pd

from datetime import date, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed


API_BASE_URL = "http://127.0.0.1:8000/api/agriculture"

FILTERS_URL = f"{API_BASE_URL}/mandi/filters"
PRICES_URL = f"{API_BASE_URL}/mandi/prices"

REQUEST_TIMEOUT = (4, 12)
MAX_WORKERS = 6

PRIORITY_COMMODITIES = [
    "Paddy", "Rice", "Ragi", "Maize", "Jowar",
    "Bajra", "Tur", "Red Gram", "Groundnut",
    "Cotton", "Sugarcane", "Onion", "Potato",
    "Tomato", "Chilli", "Turmeric", "Soyabean",
    "Arecanut", "Coconut", "Sunflower", "Wheat",
]

TEXT = {
    "kn": {
        "title": "ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು",
        "subtitle": "ನಿಮ್ಮ ಜಿಲ್ಲೆಯ ಮಾರುಕಟ್ಟೆಯ ಬೆಲೆಗಳನ್ನು ಪರಿಶೀಲಿಸಿ",
        "district": "ಜಿಲ್ಲೆ ಆಯ್ಕೆಮಾಡಿ",
        "market": "ಮಾರುಕಟ್ಟೆ / ಎಪಿಎಂಸಿ ಆಯ್ಕೆಮಾಡಿ",
        "crop": "ಬೆಳೆ ಆಯ್ಕೆಮಾಡಿ",
        "date": "ದಿನಾಂಕ ಆಯ್ಕೆಮಾಡಿ",
        "loading": "ಮಾಹಿತಿ ಲೋಡ್ ಆಗುತ್ತಿದೆ...",
        "checking": "ಈ ಮಾರುಕಟ್ಟೆಯಲ್ಲಿ ಲಭ್ಯವಿರುವ ಬೆಳೆಗಳನ್ನು ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ...",
        "no_district": "ಜಿಲ್ಲೆಗಳು ಲಭ್ಯವಿಲ್ಲ.",
        "no_market": "ಈ ಜಿಲ್ಲೆಯಲ್ಲಿ ಮಾರುಕಟ್ಟೆಗಳು ಲಭ್ಯವಿಲ್ಲ.",
        "no_crop": "ಈ ಮಾರುಕಟ್ಟೆಗೆ ವರದಿಯಾದ ಬೆಳೆ ಬೆಲೆಗಳು ಲಭ್ಯವಿಲ್ಲ.",
        "select_crop": "ಬೆಳೆ ಆಯ್ಕೆಮಾಡಿ.",
        "fetch": "ಬೆಲೆಗಳನ್ನು ಪಡೆಯಿರಿ",
        "fetching": "ಬೆಲೆಗಳನ್ನು ಪಡೆಯಲಾಗುತ್ತಿದೆ...",
        "error": "ಮಾಹಿತಿ ಪಡೆಯಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ.",
        "no_data": "ಆಯ್ಕೆ ಮಾಡಿದ ಬೆಳೆಗೆ ಬೆಲೆ ಮಾಹಿತಿ ಲಭ್ಯವಿಲ್ಲ.",
        "latest": "ಇತ್ತೀಚಿನ ಬೆಲೆ",
        "variety": "ತಳಿ",
        "unit": "ಘಟಕ",
        "reported_date": "ವರದಿಯಾದ ದಿನಾಂಕ",
        "price": "ಬೆಲೆ",
        "price_chart": "ಬೆಲೆ ಚಾರ್ಟ್",
        "price_table": "ಬೆಲೆ ವಿವರಗಳು",
        "source": "ಮೂಲ",
        "refresh": "ಮಾಹಿತಿ ಮರುಲೋಡ್ ಮಾಡಿ",
        "period": "ಲಭ್ಯವಿರುವ ಕಳೆದ 7 ದಿನಗಳ ಮಾಹಿತಿ",
        "select_all": "ಮೊದಲು ಜಿಲ್ಲೆ ಮತ್ತು ಮಾರುಕಟ್ಟೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
    },
    "en": {
        "title": "Mandi Market Prices",
        "subtitle": "Check crop prices in your district's markets",
        "district": "Select District",
        "market": "Select Market / APMC",
        "crop": "Select Crop",
        "date": "Select Date",
        "loading": "Loading information...",
        "checking": "Checking crops reported in this market...",
        "no_district": "No districts available.",
        "no_market": "No markets available in this district.",
        "no_crop": "No reported crop prices are available for this market.",
        "select_crop": "Please select a crop.",
        "fetch": "Get Prices",
        "fetching": "Fetching prices...",
        "error": "Unable to retrieve information.",
        "no_data": "No price information is available for this crop.",
        "latest": "Latest Price",
        "variety": "Variety",
        "unit": "Unit",
        "reported_date": "Reported Date",
        "price": "Price",
        "price_chart": "Price Chart",
        "price_table": "Price Details",
        "source": "Source",
        "refresh": "Refresh Information",
        "period": "Available data from the last 7 days",
        "select_all": "Please select a district and market first.",
    },
}

DISTRICT_TRANSLATIONS = {
    "ಬೆಳಗಾವಿ": "Belagavi",
    "ಬೆಂಗಳೂರು ನಗರ": "Bengaluru Urban",
    "ಬೆಂಗಳೂರು ಗ್ರಾಮಾಂತರ": "Bengaluru Rural",
    "ಬಾಗಲಕೋಟೆ": "Bagalkot",
    "ಬಳ್ಳಾರಿ": "Ballari",
    "ಬೀದರ್": "Bidar",
    "ವಿಜಯಪುರ": "Vijayapura",
    "ಚಿಕ್ಕಮಗಳೂರು": "Chikkamagaluru",
    "ಚಿತ್ರದುರ್ಗ": "Chitradurga",
    "ದಕ್ಷಿಣ ಕನ್ನಡ": "Dakshina Kannada",
    "ಧಾರವಾಡ": "Dharwad",
    "ಗದಗ": "Gadag",
    "ಹಾಸನ": "Hassan",
    "ಹಾವೇರಿ": "Haveri",
    "ಕಲಬುರಗಿ": "Kalaburagi",
    "ಕೊಡಗು": "Kodagu",
    "ಕೋಲಾರ": "Kolar",
    "ಕೊಪ್ಪಳ": "Koppal",
    "ಮಂಡ್ಯ": "Mandya",
    "ಮೈಸೂರು": "Mysuru",
    "ರಾಯಚೂರು": "Raichur",
    "ರಾಮನಗರ": "Ramanagara",
    "ಶಿವಮೊಗ್ಗ": "Shivamogga",
    "ತುಮಕೂರು": "Tumakuru",
    "ಉಡುಪಿ": "Udupi",
    "ಉತ್ತರ ಕನ್ನಡ": "Uttara Kannada",
    "ಯಾದಗಿರಿ": "Yadgir",
    "ಚಿಕ್ಕಬಳ್ಳಾಪುರ": "Chikkaballapura",
    "ವಿಜಯನಗರ": "Vijayanagara",
}

CROP_TRANSLATIONS = {
    "ಭತ್ತ": "Paddy",
    "ಅಕ್ಕಿ": "Rice",
    "ರಾಗಿ": "Ragi",
    "ಮೆಕ್ಕೆಜೋಳ": "Maize",
    "ಜೋಳ": "Jowar",
    "ಸಜ್ಜೆ": "Bajra",
    "ತೊಗರಿ": "Tur",
    "ತೊಗರಿಬೇಳೆ": "Red Gram",
    "ಶೇಂಗಾ": "Groundnut",
    "ಹತ್ತಿ": "Cotton",
    "ಕಬ್ಬು": "Sugarcane",
    "ಈರುಳ್ಳಿ": "Onion",
    "ಆಲೂಗಡ್ಡೆ": "Potato",
    "ಟೊಮೇಟೊ": "Tomato",
    "ಮೆಣಸಿನಕಾಯಿ": "Chilli",
    "ಅರಿಶಿನ": "Turmeric",
    "ಸೋಯಾಬೀನ್": "Soyabean",
    "ಅಡಿಕೆ": "Arecanut",
    "ತೆಂಗಿನಕಾಯಿ": "Coconut",
    "ಸೂರ್ಯಕಾಂತಿ": "Sunflower",
    "ಗೋಧಿ": "Wheat",
}


def get_language():
    language = st.session_state.get("language", "kn")
    return language if language in ("kn", "en") else "kn"


def tx(key):
    return TEXT[get_language()].get(key, key)


def display_name(name, translations=None):
    if get_language() == "en":
        return (translations or {}).get(name, name)
    return name


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_filters():
    response = requests.get(
        FILTERS_URL,
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()

    payload = response.json()

    if not isinstance(payload, dict):
        raise ValueError("Invalid filters response.")

    if not payload.get("success", True):
        raise ValueError(payload.get("message", "Unable to load filters."))

    data = payload.get("data", payload)

    required = ("districts", "markets", "commodities")

    for key in required:
        if not isinstance(data.get(key), list):
            raise ValueError(f"Invalid filter data: {key}")

    return data


def fetch_prices(district_id, market_id, commodity_id, selected_date):
    payload = {
        "district_id": int(district_id),
        "market_id": int(market_id),
        "commodity_id": int(commodity_id),
        "date": selected_date.isoformat(),
    }

    response = requests.post(
        PRICES_URL,
        json=payload,
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    result = response.json()

    if not isinstance(result, dict):
        raise ValueError("Invalid price response.")

    if not result.get("success", True):
        raise ValueError(result.get("message", "Unable to fetch prices."))

    return result.get("data", result)


def _check_one_commodity(
    district_id,
    market_id,
    commodity,
):
    try:
        result = fetch_prices(
            district_id,
            market_id,
            commodity["id"],
            date.today(),
        )

        if result.get("has_report"):
            return commodity

    except Exception:
        # A failed commodity request should not stop other checks.
        return None

    return None


@st.cache_data(ttl=1800, show_spinner=False)
def get_market_reported_crops(district_id, market_id, commodities):
    """
    Check commodities concurrently and return only crops
    with reported prices in the selected market.
    """

    priority = {
        name.lower()
        for name in PRIORITY_COMMODITIES
    }

    selected_commodities = sorted(
        commodities,
        key=lambda item: (
            item.get("name", "").lower() not in priority,
            item.get("name", "").lower(),
        ),
    )

    available = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(
                _check_one_commodity,
                district_id,
                market_id,
                commodity,
            ): commodity
            for commodity in selected_commodities
        }

        for future in as_completed(futures):
            try:
                commodity = future.result()

                if commodity:
                    available.append(commodity)

            except Exception:
                continue

    return sorted(
        available,
        key=lambda item: item.get("name", "").lower(),
    )


def render_price_result(result):
    if not result:
        st.warning(tx("no_data"))
        return

    if not result.get("has_report"):
        st.info(result.get("message", tx("no_data")))
        return

    st.success(result.get("message", tx("latest")))

    st.caption(
        f"{result.get('district', '')} • "
        f"{result.get('market', '')} • "
        f"{result.get('commodity', '')}"
    )

    rows = []

    for record in result.get("records", []):
        for daily in record.get("daily_prices", []):
            if daily.get("price") is not None:
                rows.append({
                    tx("variety"): record.get("variety", "Unknown"),
                    tx("reported_date"): daily.get("date"),
                    tx("price"): daily.get("price"),
                    tx("unit"): record.get("unit", "NR"),
                })

    if not rows:
        st.info(tx("no_data"))
        return

    df = pd.DataFrame(rows)

    st.subheader(tx("price_chart"))

    chart_df = df.copy()

    chart_df[tx("reported_date")] = pd.to_datetime(
        chart_df[tx("reported_date")],
        errors="coerce",
    )

    chart_df = chart_df.dropna(
        subset=[tx("reported_date"), tx("price")]
    )

    if not chart_df.empty:
        chart_data = chart_df.pivot_table(
            index=tx("reported_date"),
            columns=tx("variety"),
            values=tx("price"),
            aggfunc="mean",
        )

        st.line_chart(chart_data)

    st.subheader(tx("price_table"))
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        f"{tx('source')}: {result.get('source', 'AGMARKNET')}"
    )
    st.caption(result.get("report_period", tx("period")))


def render_mandi_page():
    st.title(tx("title"))
    st.write(tx("subtitle"))

    with st.spinner(tx("loading")):
        try:
            filters = fetch_filters()
        except Exception as error:
            st.error(f"{tx('error')} {error}")
            if st.button(tx("refresh")):
                fetch_filters.clear()
                st.rerun()
            return

    districts = filters["districts"]
    markets = filters["markets"]
    commodities = filters["commodities"]

    if not districts:
        st.warning(tx("no_district"))
        return

    district_options = {
        display_name(item["name"], DISTRICT_TRANSLATIONS): item["id"]
        for item in districts
    }

    district_label = st.selectbox(
        tx("district"),
        list(district_options.keys()),
        key="mandi_district",
    )

    district_id = district_options[district_label]

    district_markets = [
        item
        for item in markets
        if item.get("district_id") == district_id
    ]

    if not district_markets:
        st.warning(tx("no_market"))
        return

    market_options = {
        item["name"]: item["id"]
        for item in district_markets
    }

    market_label = st.selectbox(
        tx("market"),
        list(market_options.keys()),
        key="mandi_market",
    )

    market_id = market_options[market_label]

    crop_cache_key = (
        int(district_id),
        int(market_id),
    )

    if st.session_state.get("mandi_crop_cache_key") != crop_cache_key:
        st.session_state.pop("mandi_selected_crop", None)
        st.session_state["mandi_crop_cache_key"] = crop_cache_key

    with st.spinner(tx("checking")):
        try:
            available_crops = get_market_reported_crops(
                int(district_id),
                int(market_id),
                commodities,
            )
        except Exception as error:
            st.error(f"{tx('error')} {error}")
            return

    if not available_crops:
        st.info(tx("no_crop"))
        return

    crop_options = {
        display_name(item["name"], CROP_TRANSLATIONS): item["id"]
        for item in available_crops
    }

    crop_label = st.selectbox(
        tx("crop"),
        list(crop_options.keys()),
        key="mandi_selected_crop",
    )

    commodity_id = crop_options[crop_label]

    selected_date = st.date_input(
        tx("date"),
        value=date.today(),
        min_value=date.today() - timedelta(days=30),
        max_value=date.today(),
        key="mandi_selected_date",
    )

    if st.button(tx("fetch"), type="primary", use_container_width=True):
        try:
            with st.spinner(tx("fetching")):
                result = fetch_prices(
                    int(district_id),
                    int(market_id),
                    int(commodity_id),
                    selected_date,
                )

            render_price_result(result)

        except requests.Timeout:
            st.error("Request timed out. Please try again.")

        except requests.RequestException as error:
            st.error(f"{tx('error')} {error}")

        except Exception as error:
            st.error(f"{tx('error')} {error}")

    if st.button(tx("refresh")):
        fetch_filters.clear()
        get_market_reported_crops.clear()
        st.session_state.pop("mandi_crop_cache_key", None)
        st.rerun()
