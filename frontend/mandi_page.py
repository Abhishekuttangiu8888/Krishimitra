
import requests
import streamlit as st

from datetime import date, timedelta


API_BASE_URL = "http://127.0.0.1:8000/api/agriculture"


# =========================================================
# LANGUAGE TEXT
# =========================================================

TEXT = {
    "kn": {
        "title": "🌾 ಕೃಷಿ ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು",
        "subtitle": "ನಿಮ್ಮ ಆಯ್ಕೆಯ ಮಾರುಕಟ್ಟೆಯಲ್ಲಿ ವರದಿಯಾದ ಬೆಲೆಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.",
        "district": "ಜಿಲ್ಲೆ ಆಯ್ಕೆಮಾಡಿ",
        "market": "APMC ಮಾರುಕಟ್ಟೆ ಆಯ್ಕೆಮಾಡಿ",
        "crop": "ಬೆಳೆ / ಕೃಷಿ ಉತ್ಪನ್ನ ಆಯ್ಕೆಮಾಡಿ",
        "date": "ಉಲ್ಲೇಖ ದಿನಾಂಕ",
        "search": "🔍 ಮಾರುಕಟ್ಟೆ ಬೆಲೆ ಪರಿಶೀಲಿಸಿ",
        "loading_filters": "ಮಾರುಕಟ್ಟೆ ಮಾಹಿತಿಯನ್ನು ಪಡೆಯಲಾಗುತ್ತಿದೆ...",
        "loading_crops": "ಈ ಮಾರುಕಟ್ಟೆಯಲ್ಲಿ ಲಭ್ಯವಿರುವ ಬೆಳೆಗಳನ್ನು ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ...",
        "loading_prices": "ಬೆಲೆ ಮಾಹಿತಿಯನ್ನು ಪಡೆಯಲಾಗುತ್ತಿದೆ...",
        "no_markets": "ಈ ಜಿಲ್ಲೆಗೆ ಮಾರುಕಟ್ಟೆಗಳು ಲಭ್ಯವಿಲ್ಲ.",
        "no_crops": "ಈ ಮಾರುಕಟ್ಟೆಯಲ್ಲಿ ವರದಿಯಾದ ಬೆಳೆಗಳು ಲಭ್ಯವಿಲ್ಲ.",
        "no_price": "ಈ ಆಯ್ಕೆಗೆ ಬೆಲೆ ವರದಿ ಲಭ್ಯವಿಲ್ಲ.",
        "error": "ಮಾರುಕಟ್ಟೆ ಸೇವೆಯೊಂದಿಗೆ ಸಂಪರ್ಕಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ.",
        "latest": "ಇತ್ತೀಚಿನ ವರದಿಯಾದ ಬೆಲೆ",
        "date_col": "ದಿನಾಂಕ",
        "price": "ಬೆಲೆ",
        "status": "ವರದಿ ಸ್ಥಿತಿ",
        "reported": "ವರದಿಯಾಗಿದೆ",
        "not_reported": "ವರದಿ ಇಲ್ಲ",
        "source": "ಮೂಲ: AGMARKNET",
        "disclaimer": "AGMARKNET ನಲ್ಲಿ ವರದಿಯಾದ ಬೆಲೆಗಳನ್ನು ಮಾತ್ರ ತೋರಿಸಲಾಗುತ್ತದೆ.",
        "reference": "ಇತ್ತೀಚಿನ ಲಭ್ಯವಿರುವ 7 ದಿನಗಳ ವರದಿಗಳನ್ನು ತೋರಿಸಲಾಗುತ್ತದೆ.",
        "limited": "ಸದ್ಯಕ್ಕೆ ಸಾಮಾನ್ಯ ಬೆಳೆಗಳ ಪಟ್ಟಿಯನ್ನು ಮಾತ್ರ ಪರಿಶೀಲಿಸಲಾಗಿದೆ.",
    },
    "en": {
        "title": "🌾 Agricultural Mandi Prices",
        "subtitle": "Check reported agricultural prices in your selected market.",
        "district": "Select district",
        "market": "Select APMC market",
        "crop": "Select crop / commodity",
        "date": "Reference date",
        "search": "🔍 Check mandi prices",
        "loading_filters": "Loading market information...",
        "loading_crops": "Checking crops reported in this market...",
        "loading_prices": "Fetching market prices...",
        "no_markets": "No markets are available for this district.",
        "no_crops": "No reported crops were found for this market.",
        "no_price": "No price report is available for this selection.",
        "error": "Could not connect to the mandi service.",
        "latest": "Latest reported price",
        "date_col": "Date",
        "price": "Price",
        "status": "Report status",
        "reported": "Reported",
        "not_reported": "No report",
        "source": "Source: AGMARKNET",
        "disclaimer": "Only prices reported by AGMARKNET are displayed.",
        "reference": "The latest seven available reporting days are displayed.",
        "limited": "Currently, only a shortlist of common crops is checked.",
    },
}


# =========================================================
# KANNADA TRANSLATIONS
# =========================================================

KANNADA_DISTRICTS = {
    "Bagalkot": "ಬಾಗಲಕೋಟೆ",
    "Ballari": "ಬಳ್ಳಾರಿ",
    "Belagavi": "ಬೆಳಗಾವಿ",
    "Bengaluru": "ಬೆಂಗಳೂರು",
    "Bengaluru Rural": "ಬೆಂಗಳೂರು ಗ್ರಾಮಾಂತರ",
    "Bidar": "ಬೀದರ್",
    "Chamarajanagar": "ಚಾಮರಾಜನಗರ",
    "Chikkaballapur": "ಚಿಕ್ಕಬಳ್ಳಾಪುರ",
    "Chikkamagaluru": "ಚಿಕ್ಕಮಗಳೂರು",
    "Chitradurga": "ಚಿತ್ರದುರ್ಗ",
    "Dakshina Kannada": "ದಕ್ಷಿಣ ಕನ್ನಡ",
    "Davanagere": "ದಾವಣಗೆರೆ",
    "Dharwad": "ಧಾರವಾಡ",
    "Gadag": "ಗದಗ",
    "Hassan": "ಹಾಸನ",
    "Haveri": "ಹಾವೇರಿ",
    "Kalaburagi": "ಕಲಬುರಗಿ",
    "Kodagu": "ಕೊಡಗು",
    "Kolar": "ಕೋಲಾರ",
    "Koppal": "ಕೊಪ್ಪಳ",
    "Mandya": "ಮಂಡ್ಯ",
    "Mysuru": "ಮೈಸೂರು",
    "Raichur": "ರಾಯಚೂರು",
    "Ramanagara": "ರಾಮನಗರ",
    "Ramanagar": "ರಾಮನಗರ",
    "Shivamogga": "ಶಿವಮೊಗ್ಗ",
    "Tumakuru": "ತುಮಕೂರು",
    "Udupi": "ಉಡುಪಿ",
    "Uttara Kannada": "ಉತ್ತರ ಕನ್ನಡ",
    "Vijayapura": "ವಿಜಯಪುರ",
    "Vijayanagara": "ವಿಜಯನಗರ",
    "Yadgir": "ಯಾದಗಿರಿ",
}


KANNADA_CROPS = {
    "Paddy": "ಭತ್ತ",
    "Paddy(Common)": "ಸಾಮಾನ್ಯ ಭತ್ತ",
    "Rice": "ಅಕ್ಕಿ",
    "Maize": "ಮೆಕ್ಕೆಜೋಳ",
    "Ragi": "ರಾಗಿ",
    "Ragi(Finger Millet)": "ರಾಗಿ",
    "Jowar": "ಜೋಳ",
    "Jowar(Sorghum)": "ಜೋಳ",
    "Bajra": "ಸಜ್ಜೆ",
    "Wheat": "ಗೋಧಿ",
    "Groundnut": "ನೆಲಗಡಲೆ",
    "Sunflower": "ಸೂರ್ಯಕಾಂತಿ",
    "Cotton": "ಹತ್ತಿ",
    "Sugarcane": "ಕಬ್ಬು",
    "Tur": "ತೊಗರಿ",
    "Red Gram": "ತೊಗರಿ",
    "Green Gram": "ಹೆಸರುಕಾಳು",
    "Black Gram": "ಉದ್ದಿನಕಾಳು",
    "Bengal Gram": "ಕಡಲೆ",
    "Chilli": "ಮೆಣಸಿನಕಾಯಿ",
    "Dry Chilli": "ಒಣ ಮೆಣಸಿನಕಾಯಿ",
    "Onion": "ಈರುಳ್ಳಿ",
    "Tomato": "ಟೊಮೆಟೊ",
    "Potato": "ಆಲೂಗಡ್ಡೆ",
    "Coconut": "ತೆಂಗಿನಕಾಯಿ",
    "Arecanut": "ಅಡಿಕೆ",
    "Arecanut(Betelnut/Supari)": "ಅಡಿಕೆ",
    "Turmeric": "ಅರಿಶಿನ",
    "Ginger": "ಶುಂಠಿ",
    "Garlic": "ಬೆಳ್ಳುಳ್ಳಿ",
    "Cabbage": "ಎಲೆಕೋಸು",
    "Cauliflower": "ಹೂಕೋಸು",
    "Brinjal": "ಬದನೆಕಾಯಿ",
    "Beans": "ಬೀನ್ಸ್",
    "Carrot": "ಕ್ಯಾರೆಟ್",
    "Drumstick": "ನುಗ್ಗೆಕಾಯಿ",
    "Mango": "ಮಾವು",
    "Banana": "ಬಾಳೆಹಣ್ಣು",
    "Papaya": "ಪಪ್ಪಾಯಿ",
    "Lemon": "ನಿಂಬೆಹಣ್ಣು",
    "Chana": "ಕಡಲೆ",
    "Soyabean": "ಸೋಯಾಬೀನ್",
    "Mustard": "ಸಾಸಿವೆ",
    "Sesamum": "ಎಳ್ಳು",
    "Castor Seed": "ಹರಳು",
}


# =========================================================
# TEMPORARY COMMODITY CHECK LIMIT
# =========================================================

# This is a shortlist, NOT a complete list of market crops.
PRIORITY_COMMODITY_IDS = {
    2,    # Paddy
    4,    # Maize
    5,    # Jowar
    23,   # Onion
    24,   # Potato
    30,   # Ragi
    35,   # Turmeric
    65,   # Tomato
    116,  # Coconut
    118,  # Arecanut
}


# =========================================================
# LANGUAGE HELPERS
# =========================================================

def get_language():
    keys = [
        "language",
        "selected_language",
        "app_language",
        "ui_language",
        "locale",
    ]

    for key in keys:
        value = st.session_state.get(key)

        if not isinstance(value, str):
            continue

        value = value.lower().strip()

        if value in ("kn", "kn-in", "kannada", "ಕನ್ನಡ"):
            return "kn"

        if value in ("en", "en-in", "english", "ಇಂಗ್ಲಿಷ್"):
            return "en"

    return "kn"


def tr(key):
    return TEXT[get_language()].get(key, key)


def display_district(name):
    if get_language() == "kn":
        return KANNADA_DISTRICTS.get(name, name)

    return name


def display_crop(name):
    if get_language() == "kn":
        return KANNADA_CROPS.get(name, name)

    return name


# =========================================================
# FETCH FILTERS — ONLY ONE DEFINITION
# =========================================================

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_filters():
    try:
        response = requests.get(
            f"{API_BASE_URL}/mandi/filters",
            timeout=30,
        )

        response.raise_for_status()
        result = response.json()

        if result.get("success"):
            return result.get("data")

        return None

    except requests.RequestException:
        return None

    except ValueError:
        return None


# =========================================================
# FETCH MARKET PRICES
# =========================================================

def fetch_prices(
    district_id,
    market_id,
    commodity_id,
    selected_date,
):
    payload = {
        "district_id": district_id,
        "market_id": market_id,
        "commodity_id": commodity_id,
        "selected_date": selected_date.isoformat(),
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/mandi/prices",
            json=payload,
            timeout=30,
        )

        if response.status_code == 503:
            return None, tr("no_price")

        response.raise_for_status()

        result = response.json()

        if result.get("success"):
            return result.get("data"), None

        return None, tr("no_price")

    except requests.Timeout:
        return None, tr("error")

    except requests.RequestException:
        return None, tr("error")

    except ValueError:
        return None, tr("error")


# =========================================================
# CHECK MARKET-SPECIFIC CROPS
# =========================================================

@st.cache_data(ttl=1800, show_spinner=False)
def get_market_reported_crops(
    district_id,
    market_id,
    commodities,
):
    available_crops = []

    candidates = [
        item
        for item in commodities
        if item.get("id") in PRIORITY_COMMODITY_IDS
    ]

    for commodity in candidates:
        try:
            response = requests.post(
                f"{API_BASE_URL}/mandi/prices",
                json={
                    "district_id": district_id,
                    "market_id": market_id,
                    "commodity_id": commodity["id"],
                    "selected_date": date.today().isoformat(),
                },
                timeout=20,
            )

            # Stop checking if AGMARKNET/service is unavailable.
            if response.status_code == 503:
                break

            response.raise_for_status()
            result = response.json()

            if not result.get("success"):
                continue

            data = result.get("data") or {}
            records = data.get("records", [])

            has_report = any(
                record.get("has_report")
                and any(
                    day.get("reported")
                    and day.get("price") is not None
                    for day in record.get("daily_prices", [])
                )
                for record in records
            )

            if has_report:
                available_crops.append(commodity)

        except (
            requests.RequestException,
            ValueError,
            TypeError,
        ):
            continue

    return available_crops


# =========================================================
# DISPLAY PRICE RESULTS
# =========================================================


def render_price_result(result):

    records = result.get("records", [])

    if not records or not result.get("has_report"):
        st.info(tr("no_price"))
        return

    commodity_name = display_crop(result.get("commodity", ""))

    st.markdown(
        f"""
        <div class="price-result-heading">
            <h3>{commodity_name}</h3>
            <p>{result.get("market", "")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for index, record in enumerate(records):

        st.markdown(f"### {record.get('variety', '—')}")

        latest_price = record.get("latest_price")
        latest_date = record.get("latest_date")

        if latest_price is not None:
            st.metric(
                tr("latest"),
                f"₹{latest_price:,.2f}",
                help=f"{tr('date_col')}: {latest_date}",
            )

        daily_prices = record.get("daily_prices", [])

        table_rows = []

        for item in daily_prices:
            price = item.get("price")

            table_rows.append({
                tr("date_col"): item.get("date", "—"),
                tr("price"): (
                    f"₹{price:,.2f}" if price is not None else "—"
                ),
                tr("status"): (
                    tr("reported")
                    if item.get("reported")
                    else tr("not_reported")
                ),
            })

        if table_rows:
            st.markdown(
                "#### " + tr("date_col") + " / " + tr("price")
            )

            headers = list(table_rows[0].keys())

            header_cols = st.columns(len(headers))

            for col, header in zip(header_cols, headers):
                col.markdown(f"**{header}**")

            for row in table_rows:
                cols = st.columns(len(headers))

                for col, header in zip(cols, headers):
                    col.write(row[header])

        chart_data = [
            {
                "Date": item.get("date"),
                "Price": item.get("price"),
            }
            for item in daily_prices
            if (
                item.get("reported")
                and item.get("price") is not None
            )
        ]

        if chart_data:
            chart_data.reverse()

            st.markdown("#### Price trend")

            st.line_chart(
                chart_data,
                x="Date",
                y="Price",
            )

        if index < len(records) - 1:
            st.divider()

    st.caption(tr("source"))
    st.info(tr("disclaimer"))


# =========================================================
# MAIN MANDI PAGE
# =========================================================

def render_mandi_page():

    # -----------------------------------------------------
    # PAGE STYLING
    # -----------------------------------------------------

    st.markdown(
        """
        <style>

        .mandi-header {
            background: linear-gradient(
                120deg,
                #e8f5e9,
                #f1f8e9
            );
            padding: 28px;
            border-radius: 18px;
            margin-bottom: 25px;
            border: 1px solid #d7ead8;
        }

        .mandi-header h1 {
            color: #1b5e20;
            font-size: 32px;
            font-weight: 800;
            margin: 0;
        }

        .mandi-header p {
            color: #45634a;
            font-size: 17px;
            margin-top: 10px;
            margin-bottom: 0;
        }

        .mandi-section-heading {
            color: #263b2b;
            font-size: 23px;
            font-weight: 750;
            margin-top: 15px;
            margin-bottom: 18px;
        }

        .price-result-heading {
            background: #edf7ed;
            border-left: 5px solid #2e7d32;
            border-radius: 10px;
            padding: 16px 20px;
            margin-top: 20px;
            margin-bottom: 18px;
        }

        .price-result-heading h3 {
            color: #1b5e20;
            margin: 0;
        }

        .price-result-heading p {
            color: #526b55;
            margin-top: 5px;
            margin-bottom: 0;
        }

        .stApp label {
            font-size: 16px !important;
            font-weight: 600 !important;
        }

        div[data-testid="stSelectbox"] {
            margin-bottom: 15px;
        }

        div[data-testid="stSelectbox"] div[role="combobox"] {
            min-height: 48px;
            border-radius: 9px;
        }

        .st-key-mandi_search_button button {
            background-color: #218838 !important;
            color: #ffffff !important;
            border: 1px solid #218838 !important;
            border-radius: 10px !important;
            width: 100% !important;
            min-height: 54px !important;
            font-size: 17px !important;
            font-weight: 700 !important;
            opacity: 1 !important;
            visibility: visible !important;
            box-shadow: 0 3px 8px rgba(0,0,0,0.12) !important;
        }

        .st-key-mandi_search_button button:hover {
            background-color: #176b2c !important;
            color: #ffffff !important;
        }

        .st-key-mandi_search_button button p {
            color: #ffffff !important;
        }

        div[data-testid="stMetric"] {
            background: #f1f8f1;
            border: 1px solid #d9ead9;
            padding: 16px;
            border-radius: 12px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    st.markdown(
        f"""
        <div class="mandi-header">
            <h1>{tr("title")}</h1>
            <p>{tr("subtitle")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # LOAD FILTERS
    # -----------------------------------------------------

    with st.spinner(tr("loading_filters")):
        filters = fetch_filters()

    if not filters:
        st.error(tr("error"))
        return

    districts = filters.get("districts", [])
    markets = filters.get("markets", [])
    commodities = filters.get("commodities", [])

    if not districts:
        st.warning(tr("no_markets"))
        return

    # -----------------------------------------------------
    # DISTRICT SELECT
    # -----------------------------------------------------

    st.markdown(
        f"""
        <div class="mandi-section-heading">
            📍 {tr("district")}
        </div>
        """,
        unsafe_allow_html=True,
    )

    district_names = [
        item["name"]
        for item in districts
        if item.get("name")
    ]

    if not district_names:
        st.warning(tr("no_markets"))
        return

    district_name = st.selectbox(
        tr("district"),
        district_names,
        format_func=display_district,
        key="mandi_district",
    )

    selected_district = next(
        item
        for item in districts
        if item["name"] == district_name
    )

    district_id = selected_district["id"]

    # -----------------------------------------------------
    # MARKET SELECT
    # -----------------------------------------------------

    district_markets = [
        item
        for item in markets
        if item.get("district_id") == district_id
    ]

    if not district_markets:
        st.warning(tr("no_markets"))
        return

    market_names = [
        item["name"]
        for item in district_markets
        if item.get("name")
    ]

    if not market_names:
        st.warning(tr("no_markets"))
        return

    market_name = st.selectbox(
        tr("market"),
        market_names,
        key=f"mandi_market_{district_id}",
    )

    selected_market = next(
        item
        for item in district_markets
        if item["name"] == market_name
    )

    market_id = selected_market["id"]

    # -----------------------------------------------------
    # MARKET-SPECIFIC CROPS
    # -----------------------------------------------------

    st.divider()

    cache_key = f"mandi_crops_{district_id}_{market_id}"

    if cache_key not in st.session_state:

        with st.spinner(tr("loading_crops")):
            available_crops = get_market_reported_crops(
                district_id,
                market_id,
                commodities,
            )

        st.session_state[cache_key] = available_crops

    available_crops = st.session_state[cache_key]

    if not available_crops:
        st.warning(tr("no_crops"))
        return

    st.caption(tr("limited"))

    crop_options = {
        item["name"]: item
        for item in available_crops
        if item.get("name")
    }

    if not crop_options:
        st.warning(tr("no_crops"))
        return

    crop_name = st.selectbox(
        tr("crop"),
        list(crop_options.keys()),
        format_func=display_crop,
        key=f"mandi_crop_{district_id}_{market_id}",
    )

    selected_commodity = crop_options[crop_name]
    commodity_id = selected_commodity["id"]

    # -----------------------------------------------------
    # DATE SELECT
    # -----------------------------------------------------

    today = date.today()

    selected_date = st.date_input(
        tr("date"),
        value=today,
        min_value=today - timedelta(days=30),
        max_value=today,
        key="mandi_selected_date",
    )

    st.caption(tr("reference"))

    # -----------------------------------------------------
    # SEARCH BUTTON
    # -----------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        tr("search"),
        type="primary",
        use_container_width=True,
        key="mandi_search_button",
    ):

        with st.spinner(tr("loading_prices")):
            result, error = fetch_prices(
                district_id,
                market_id,
                commodity_id,
                selected_date,
            )

        if error:
            st.warning(error)

        elif result:
            render_price_result(result)

        else:
            st.info(tr("no_price"))
