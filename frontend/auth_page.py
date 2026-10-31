
import requests
import streamlit as st

from frontend.voice_registration import render_voice_registration
from frontend.i18n import set_language


API_URL = "http://127.0.0.1:8000/api"


DISTRICTS = [
    "Bagalkote", "Ballari", "Belagavi", "Bengaluru Rural",
    "Bengaluru Urban", "Bidar", "Chamarajanagar", "Chikkaballapur",
    "Chikkamagaluru", "Chitradurga", "Dakshina Kannada",
    "Davanagere", "Dharwad", "Gadag", "Hassan", "Haveri",
    "Kalaburagi", "Kodagu", "Kolar", "Koppal", "Mandya",
    "Mysuru", "Raichur", "Ramanagara", "Shivamogga",
    "Tumakuru", "Udupi", "Uttara Kannada", "Vijayanagara",
    "Vijayapura", "Yadgir"
]


TEXT = {
    "kn": {
        "title": "🌱 ಕೃಷಿ ಮಿತ್ರ",
        "tagline": "ನಿಮ್ಮ AI ಕೃಷಿ ಸಹಾಯಕ",
        "signup": "ನೋಂದಣಿ",
        "login": "ಲಾಗಿನ್",
        "step": "ಹಂತ",
        "next": "ಮುಂದೆ",
        "back": "ಹಿಂದೆ",
        "submit": "ಖಾತೆ ರಚಿಸಿ",
        "name": "ಪೂರ್ಣ ಹೆಸರು",
        "mobile": "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ",
        "password": "ಪಾಸ್‌ವರ್ಡ್",
        "confirm": "ಪಾಸ್‌ವರ್ಡ್ ದೃಢೀಕರಿಸಿ",
        "district": "ಜಿಲ್ಲೆ ಆಯ್ಕೆಮಾಡಿ",
        "language": "ಭಾಷೆ",
        "land": "ಜಮೀನಿನ ವಿಸ್ತೀರ್ಣ",
        "unit": "ಅಳತೆಯ ಘಟಕ",
        "ownership": "ಜಮೀನಿನ ಮಾಲೀಕತ್ವ",
        "crops": "ಬೆಳೆಯುವ ಬೆಳೆಗಳು",
        "irrigation": "ನೀರಾವರಿ ವಿಧಾನ",
        "farming": "ಕೃಷಿ ವಿಧಾನ",
        "needs": "ನಿಮಗೆ ಬೇಕಾದ ಸೇವೆಗಳು",
        "choose": "ಆಯ್ಕೆಮಾಡಿ",

        "land_units": {
            "Acre": "ಎಕರೆ",
            "Hectare": "ಹೆಕ್ಟೇರ್",
            "Gunta": "ಗುಂಟೆ",
        },

        "ownership_options": {
            "Owned": "ಸ್ವಂತ ಜಮೀನು",
            "Leased": "ಗುತ್ತಿಗೆ ಜಮೀನು",
            "Shared": "ಹಂಚಿಕೆಯ ಜಮೀನು",
        },

        "crop_options": {
            "Paddy": "ಭತ್ತ",
            "Ragi": "ರಾಗಿ",
            "Maize": "ಮೆಕ್ಕೆಜೋಳ",
            "Sugarcane": "ಕಬ್ಬು",
            "Cotton": "ಹತ್ತಿ",
            "Groundnut": "ನೆಲಗಡಲೆ",
            "Arecanut": "ಅಡಿಕೆ",
            "Other": "ಇತರೆ",
        },

        "irrigation_options": {
            "Rainfed": "ಮಳೆ ಆಧಾರಿತ",
            "Borewell": "ಬೋರ್‌ವೆಲ್",
            "Canal": "ಕಾಲುವೆ",
            "Drip": "ಹನಿ ನೀರಾವರಿ",
            "Other": "ಇತರೆ",
        },

        "farming_options": {
            "Traditional": "ಸಾಂಪ್ರದಾಯಿಕ ಕೃಷಿ",
            "Organic": "ಸಾವಯವ ಕೃಷಿ",
            "Mixed": "ಮಿಶ್ರ ಕೃಷಿ",
            "Commercial": "ವಾಣಿಜ್ಯ ಕೃಷಿ",
        },

        "needs_options": {
            "Government schemes": "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು",
            "Mandi prices": "ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು",
            "Crop disease help": "ಬೆಳೆ ರೋಗಗಳ ಮಾಹಿತಿ",
            "Weather": "ಹವಾಮಾನ ಮಾಹಿತಿ",
            "Crop planning": "ಬೆಳೆ ಯೋಜನೆ",
        },

        "required": "ದಯವಿಟ್ಟು ಈ ಹಂತದ ಎಲ್ಲಾ ಅಗತ್ಯ ಮಾಹಿತಿಯನ್ನು ಭರ್ತಿ ಮಾಡಿ.",
        "password_error": "ಎರಡೂ ಪಾಸ್‌ವರ್ಡ್‌ಗಳು ಒಂದೇ ಆಗಿರಬೇಕು.",
        "success": "ನೋಂದಣಿ ಯಶಸ್ವಿಯಾಗಿದೆ!",
        "login_mobile": "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ",
        "login_password": "ಪಾಸ್‌ವರ್ಡ್",
        "login_button": "ಲಾಗಿನ್",
        "account_heading": "ನಿಮ್ಮ ಖಾತೆಯನ್ನು ರಚಿಸಿ",
        "location_heading": "ನಿಮ್ಮ ಸ್ಥಳದ ಮಾಹಿತಿ",
        "farm_heading": "ಕೃಷಿ ಮಾಹಿತಿ",
        "review_heading": "ಮಾಹಿತಿಯನ್ನು ಪರಿಶೀಲಿಸಿ",
        "land_error": "ಜಮೀನಿನ ವಿಸ್ತೀರ್ಣವನ್ನು ನಮೂದಿಸಿ.",
        "select_error": "ದಯವಿಟ್ಟು ಆಯ್ಕೆಯನ್ನು ಮಾಡಿ.",
        "crops_error": "ಕನಿಷ್ಠ ಒಂದು ಬೆಳೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
        "needs_error": "ಕನಿಷ್ಠ ಒಂದು ಸೇವೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
        "mobile_error": "ಸರಿಯಾದ 10 ಅಂಕಿಯ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ.",
        "password_length_error": "ಪಾಸ್‌ವರ್ಡ್ ಕನಿಷ್ಠ 8 ಅಕ್ಷರಗಳಿರಬೇಕು.",
        "voice_signup": "🎙️ ಧ್ವನಿ ಮೂಲಕ ನೋಂದಣಿ",
        "server_error": "ಸರ್ವರ್ ಸಂಪರ್ಕ ದೋಷ. ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "district_placeholder": "ಜಿಲ್ಲೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "language_label": "ಭಾಷೆ / Language",
    },

    "en": {
        "title": "🌱 KRISHI MITRA",
        "tagline": "Your AI-powered agricultural companion",
        "signup": "Sign Up",
        "login": "Login",
        "step": "Step",
        "next": "Next",
        "back": "Back",
        "submit": "Create Account",
        "name": "Full name",
        "mobile": "Mobile number",
        "password": "Password",
        "confirm": "Confirm password",
        "district": "Select district",
        "language": "Preferred language",
        "land": "Land area",
        "unit": "Land unit",
        "ownership": "Land ownership",
        "crops": "Crops grown",
        "irrigation": "Irrigation method",
        "farming": "Farming type",
        "needs": "Services you need",
        "choose": "Select",

        "land_units": {
            "Acre": "Acre",
            "Hectare": "Hectare",
            "Gunta": "Gunta",
        },

        "ownership_options": {
            "Owned": "Owned land",
            "Leased": "Leased land",
            "Shared": "Shared land",
        },

        "crop_options": {
            "Paddy": "Paddy",
            "Ragi": "Ragi",
            "Maize": "Maize",
            "Sugarcane": "Sugarcane",
            "Cotton": "Cotton",
            "Groundnut": "Groundnut",
            "Arecanut": "Arecanut",
            "Other": "Other",
        },

        "irrigation_options": {
            "Rainfed": "Rainfed",
            "Borewell": "Borewell",
            "Canal": "Canal",
            "Drip": "Drip irrigation",
            "Other": "Other",
        },

        "farming_options": {
            "Traditional": "Traditional",
            "Organic": "Organic",
            "Mixed": "Mixed farming",
            "Commercial": "Commercial",
        },

        "needs_options": {
            "Government schemes": "Government schemes",
            "Mandi prices": "Mandi prices",
            "Crop disease help": "Crop disease help",
            "Weather": "Weather",
            "Crop planning": "Crop planning",
        },

        "required": "Please complete all required fields in this step.",
        "password_error": "Both passwords must match.",
        "success": "Registration successful!",
        "login_mobile": "Mobile number",
        "login_password": "Password",
        "login_button": "Login",
        "account_heading": "Create your account",
        "location_heading": "Your location",
        "farm_heading": "Farming details",
        "review_heading": "Review your information",
        "land_error": "Please enter your land area.",
        "select_error": "Please select an option.",
        "crops_error": "Select at least one crop.",
        "needs_error": "Select at least one service.",
        "mobile_error": "Enter a valid 10-digit mobile number.",
        "password_length_error": "Password must be at least 8 characters.",
        "voice_signup": "🎙️ Voice Registration",
        "server_error": "Server connection error. Please try again.",
        "district_placeholder": "Choose a district",
        "language_label": "Language",
    }
}


# ---------------------------------------------------------
# INITIALIZE FORM
# ---------------------------------------------------------

def initialize_form():
    defaults = {
        "km_language": st.session_state.get("language", "kn"),
        "km_signup_step": 1,
        "km_signup_data": {},
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state.km_language not in TEXT:
        st.session_state.km_language = "kn"

    # Keep the global app language synchronized.
    set_language(st.session_state.km_language)


def field(key, label, default=""):
    return st.text_input(
        label,
        value=st.session_state.km_signup_data.get(key, default),
        key=f"signup_{key}",
    )


def save_step(values):
    st.session_state.km_signup_data.update(values)


def change_auth_language():
    selected = st.session_state.km_language_selector
    new_language = "kn" if selected == "ಕನ್ನಡ" else "en"

    st.session_state.km_language = new_language
    set_language(new_language)


def show_server_error():
    lang = st.session_state.km_language
    st.error(TEXT[lang]["server_error"])


# ---------------------------------------------------------
# MAIN AUTHENTICATION PAGE
# ---------------------------------------------------------

def render_auth_page():

    initialize_form()

    lang = st.session_state.km_language
    t = TEXT[lang]

    # HEADER AND LANGUAGE SELECTION
    left, right = st.columns([3, 1])

    with left:
        st.markdown(f"# {t['title']}")
        st.caption(t["tagline"])

    with right:
        st.selectbox(
            t["language_label"],
            options=["ಕನ್ನಡ", "English"],
            index=0 if lang == "kn" else 1,
            key="km_language_selector",
            on_change=change_auth_language,
        )

    st.divider()

    # AUTHENTICATION TABS
    signup_tab, voice_tab, login_tab = st.tabs([
        t["signup"],
        t["voice_signup"],
        t["login"],
    ])

    # -----------------------------------------------------
    # NORMAL SIGNUP
    # -----------------------------------------------------

    with signup_tab:

        step = st.session_state.km_signup_step
        data = st.session_state.km_signup_data

        st.progress(step / 4)
        st.caption(f"{t['step']} {step} / 4")

        # STEP 1: ACCOUNT DETAILS
        if step == 1:

            st.subheader(t["account_heading"])

            name = field("full_name", t["name"])
            mobile = field("mobile", t["mobile"])

            password = st.text_input(
                t["password"],
                type="password",
                key="signup_password",
            )

            confirm = st.text_input(
                t["confirm"],
                type="password",
                key="signup_confirm",
            )

            if st.button(
                t["next"],
                type="primary",
                use_container_width=True,
                key="signup_step1_next",
            ):

                if not name.strip() or not mobile.strip() or not password or not confirm:
                    st.error(t["required"])

                elif not mobile.isdigit() or len(mobile) != 10:
                    st.error(t["mobile_error"])

                elif len(password) < 8:
                    st.error(t["password_length_error"])

                elif password != confirm:
                    st.error(t["password_error"])

                else:
                    save_step({
                        "full_name": name.strip(),
                        "mobile": mobile.strip(),
                        "password": password,
                    })

                    st.session_state.km_signup_step = 2
                    st.rerun()

        # STEP 2: LOCATION
        elif step == 2:

            st.subheader(t["location_heading"])

            district = st.selectbox(
                t["district"],
                options=DISTRICTS,
                index=None,
                placeholder=t["district_placeholder"],
                key="signup_district",
            )

            if st.button(
                t["next"],
                type="primary",
                use_container_width=True,
                key="signup_step2_next",
            ):

                if not district:
                    st.error(t["required"])

                else:
                    save_step({
                        "state": "Karnataka",
                        "district": district,
                    })

                    st.session_state.km_signup_step = 3
                    st.rerun()

        # STEP 3: FARM DETAILS
        elif step == 3:

            st.subheader(t["farm_heading"])

            land_area = st.number_input(
                t["land"],
                min_value=0.0,
                value=0.0,
                step=0.1,
                key="signup_land_area",
            )

            land_unit = st.selectbox(
                t["unit"],
                options=list(t["land_units"].keys()),
                format_func=lambda value: t["land_units"][value],
                index=None,
                placeholder=t["choose"],
                key="signup_land_unit",
            )

            ownership = st.selectbox(
                t["ownership"],
                options=list(t["ownership_options"].keys()),
                format_func=lambda value: t["ownership_options"][value],
                index=None,
                placeholder=t["choose"],
                key="signup_ownership",
            )

            crops = st.multiselect(
                t["crops"],
                options=list(t["crop_options"].keys()),
                format_func=lambda value: t["crop_options"][value],
                key="signup_crops",
            )

            irrigation = st.selectbox(
                t["irrigation"],
                options=list(t["irrigation_options"].keys()),
                format_func=lambda value: t["irrigation_options"][value],
                index=None,
                placeholder=t["choose"],
                key="signup_irrigation",
            )

            farming_type = st.selectbox(
                t["farming"],
                options=list(t["farming_options"].keys()),
                format_func=lambda value: t["farming_options"][value],
                index=None,
                placeholder=t["choose"],
                key="signup_farming_type",
            )

            needs = st.multiselect(
                t["needs"],
                options=list(t["needs_options"].keys()),
                format_func=lambda value: t["needs_options"][value],
                key="signup_needs",
            )

            if st.button(
                t["next"],
                type="primary",
                use_container_width=True,
                key="signup_step3_next",
            ):

                if land_area <= 0:
                    st.error(t["land_error"])

                elif not land_unit or not ownership or not irrigation or not farming_type:
                    st.error(t["select_error"])

                elif not crops:
                    st.error(t["crops_error"])

                elif not needs:
                    st.error(t["needs_error"])

                else:
                    save_step({
                        "land_area": str(land_area),
                        "land_unit": land_unit,
                        "land_ownership": ownership,
                        "crops": crops,
                        "irrigation_method": irrigation,
                        "farming_type": farming_type,
                        "needs": needs,
                        "preferred_language": lang,
                    })

                    st.session_state.km_signup_step = 4
                    st.rerun()

        # STEP 4: REVIEW AND SUBMIT
        elif step == 4:

            st.subheader(t["review_heading"])

            st.write(f"**{t['name']}:** {data.get('full_name', '')}")
            st.write(f"**{t['mobile']}:** {data.get('mobile', '')}")
            st.write(f"**{t['district']}:** {data.get('district', '')}")

            st.write(
                f"**{t['land']}:** "
                f"{data.get('land_area', '')} "
                f"{t['land_units'].get(data.get('land_unit', ''), '')}"
            )

            translated_crops = [
                t["crop_options"].get(crop, crop)
                for crop in data.get("crops", [])
            ]

            st.write(f"**{t['crops']}:** {', '.join(translated_crops)}")

            if st.button(
                t["submit"],
                type="primary",
                use_container_width=True,
                key="signup_create_account",
            ):

                profile_payload = {
                    "full_name": data["full_name"],
                    "preferred_language": data.get("preferred_language", lang),
                    "state": data.get("state", "Karnataka"),
                    "district": data["district"],
                    "land_area": str(data["land_area"]),
                    "land_unit": data["land_unit"],
                    "land_ownership": data["land_ownership"],
                    "crops": data["crops"],
                    "irrigation_method": data["irrigation_method"],
                    "farming_type": data["farming_type"],
                    "needs": data["needs"],
                }

                payload = {
                    "mobile": data["mobile"],
                    "password": data["password"],
                    "profile": profile_payload,
                }

                try:
                    response = requests.post(
                        f"{API_URL}/auth/signup",
                        json=payload,
                        timeout=20,
                    )

                    if response.status_code in [200, 201]:

                        result = response.json()

                        st.session_state.km_token = result["access_token"]
                        st.session_state.km_mobile = data["mobile"]
                        st.session_state.km_logged_in = True

                        st.session_state.km_signup_data = {}
                        st.session_state.km_signup_step = 1

                        st.success(t["success"])
                        st.rerun()

                    else:
                        try:
                            detail = response.json().get("detail", response.text)
                        except ValueError:
                            detail = response.text

                        st.error(detail)

                except requests.RequestException:
                    show_server_error()

        # BACK BUTTON
        if step > 1:

            if st.button(
                t["back"],
                use_container_width=True,
                key="signup_back",
            ):
                st.session_state.km_signup_step -= 1
                st.rerun()

    # -----------------------------------------------------
    # VOICE REGISTRATION
    # -----------------------------------------------------

    with voice_tab:
        render_voice_registration()

    # -----------------------------------------------------
    # LOGIN
    # -----------------------------------------------------

    with login_tab:

        st.subheader(t["login"])

        mobile = st.text_input(
            t["login_mobile"],
            key="login_mobile",
        )

        password = st.text_input(
            t["login_password"],
            type="password",
            key="login_password",
        )

        if st.button(
            t["login_button"],
            type="primary",
            use_container_width=True,
            key="login_submit",
        ):

            if not mobile or not password:
                st.error(t["required"])

            else:
                try:
                    response = requests.post(
                        f"{API_URL}/auth/login",
                        json={
                            "mobile": mobile,
                            "password": password,
                        },
                        timeout=20,
                    )

                    if response.status_code == 200:

                        result = response.json()

                        st.session_state.km_token = result["access_token"]
                        st.session_state.km_mobile = mobile
                        st.session_state.km_logged_in = True

                        st.rerun()

                    else:
                        try:
                            detail = response.json().get("detail", response.text)
                        except ValueError:
                            detail = response.text

                        st.error(detail)

                except requests.RequestException:
                    show_server_error()
