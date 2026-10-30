
import streamlit as st

from frontend.i18n import get_current_language, t


PROFILE_TEXT = {
    "kn": {
        "intro": "ನಿಮ್ಮ ಕೃಷಿ ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ. ಇದರಿಂದ ಸೂಕ್ತ ಕೃಷಿ ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಲು ಸಹಾಯವಾಗುತ್ತದೆ.",
        "personal": "ವೈಯಕ್ತಿಕ ಮಾಹಿತಿ",
        "location": "ಸ್ಥಳದ ವಿವರಗಳು",
        "farming": "ಕೃಷಿ ವಿವರಗಳು",
        "name": "ರೈತರ ಹೆಸರು",
        "phone": "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ (ಐಚ್ಛಿಕ)",
        "state": "ರಾಜ್ಯ",
        "district": "ಜಿಲ್ಲೆ",
        "taluk": "ತಾಲೂಕು",
        "village": "ಗ್ರಾಮ",
        "land": "ಜಮೀನಿನ ವಿಸ್ತೀರ್ಣ",
        "unit": "ಅಳತೆಯ ಘಟಕ",
        "ownership": "ಜಮೀನಿನ ಮಾಲೀಕತ್ವ",
        "crop": "ಮುಖ್ಯ ಬೆಳೆ",
        "irrigation": "ನೀರಾವರಿ ವಿಧಾನ",
        "needs": "ನಿಮ್ಮ ಕೃಷಿ ಅಗತ್ಯಗಳು",
        "save": "ಪ್ರೊಫೈಲ್ ಉಳಿಸಿ",
        "saved": "ನಿಮ್ಮ ರೈತ ಪ್ರೊಫೈಲ್ ಯಶಸ್ವಿಯಾಗಿ ಉಳಿಸಲಾಗಿದೆ.",
        "required": "ದಯವಿಟ್ಟು ಹೆಸರು, ಜಿಲ್ಲೆ ಮತ್ತು ಗ್ರಾಮವನ್ನು ನಮೂದಿಸಿ.",
        "summary": "ಉಳಿಸಿದ ಪ್ರೊಫೈಲ್ ವಿವರಗಳು",
        "edit": "ಮಾಹಿತಿಯನ್ನು ಬದಲಾಯಿಸಿ ಮತ್ತು ಮತ್ತೆ ಉಳಿಸಿ",
        "select": "ಆಯ್ಕೆಮಾಡಿ",
        "other": "ಇತರೆ",
        "ownership_options": ["ಸ್ವಂತ ಜಮೀನು", "ಗುತ್ತಿಗೆ ಜಮೀನು", "ಹಂಚಿಕೆ ಕೃಷಿ", "ಇತರೆ"],
        "irrigation_options": ["ಮಳೆ ಆಧಾರಿತ", "ಬೋರ್‌ವೆಲ್", "ಬಾವಿ", "ಕಾಲುವೆ", "ಹನಿ ನೀರಾವರಿ", "ಸಿಂಪಡಣೆ ನೀರಾವರಿ", "ಇತರೆ"],
        "crop_options": ["ಭತ್ತ", "ರಾಗಿ", "ಜೋಳ", "ಮೆಕ್ಕೆಜೋಳ", "ಕಬ್ಬು", "ಹತ್ತಿ", "ಅಡಿಕೆ", "ತೆಂಗು", "ದ್ವಿದಳ ಧಾನ್ಯಗಳು", "ತರಕಾರಿಗಳು", "ಇತರೆ"],
        "need_options": ["ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು", "ಬೆಳೆ ಸಾಲ", "ಬೀಜ ಮತ್ತು ಗೊಬ್ಬರ", "ಬೆಳೆ ರೋಗ ಮಾಹಿತಿ", "ಮಾರುಕಟ್ಟೆ ಬೆಲೆ", "ನೀರಾವರಿ ಸಹಾಯ", "ಹವಾಮಾನ ಮಾಹಿತಿ"],
        "acres": "ಎಕರೆ",
        "hectares": "ಹೆಕ್ಟೇರ್",
        "karnataka": "ಕರ್ನಾಟಕ",
    },
    "en": {
        "intro": "Enter your farming details. This will help us find relevant agricultural schemes and services.",
        "personal": "Personal information",
        "location": "Location details",
        "farming": "Farming details",
        "name": "Farmer name",
        "phone": "Mobile number (optional)",
        "state": "State",
        "district": "District",
        "taluk": "Taluk",
        "village": "Village",
        "land": "Land area",
        "unit": "Measurement unit",
        "ownership": "Land ownership",
        "crop": "Main crop",
        "irrigation": "Irrigation method",
        "needs": "Your farming needs",
        "save": "Save profile",
        "saved": "Your farmer profile has been saved successfully.",
        "required": "Please enter your name, district and village.",
        "summary": "Saved profile details",
        "edit": "Edit your information and save again",
        "select": "Select",
        "other": "Other",
        "ownership_options": ["Owned land", "Leased land", "Sharecropping", "Other"],
        "irrigation_options": ["Rain-fed", "Borewell", "Well", "Canal", "Drip irrigation", "Sprinkler irrigation", "Other"],
        "crop_options": ["Rice", "Ragi", "Jowar", "Maize", "Sugarcane", "Cotton", "Arecanut", "Coconut", "Pulses", "Vegetables", "Other"],
        "need_options": ["Government schemes", "Crop loan", "Seeds and fertilizers", "Crop disease information", "Market prices", "Irrigation support", "Weather information"],
        "acres": "Acres",
        "hectares": "Hectares",
        "karnataka": "Karnataka",
    },
}


KARNATAKA_DISTRICTS = [
    "Bagalkot", "Ballari", "Belagavi", "Bengaluru Rural",
    "Bengaluru Urban", "Bidar", "Chamarajanagar", "Chikkaballapur",
    "Chikkamagaluru", "Chitradurga", "Dakshina Kannada",
    "Davanagere", "Dharwad", "Gadag", "Hassan", "Haveri",
    "Kalaburagi", "Kodagu", "Kolar", "Koppal", "Mandya",
    "Mysuru", "Raichur", "Ramanagara", "Shivamogga",
    "Tumakuru", "Udupi", "Uttara Kannada", "Vijayanagara",
    "Vijayapura", "Yadgir",
]


def _show_saved_profile(profile, labels):
    st.markdown(f"### ✅ {labels['summary']}")

    rows = [
        (labels["name"], profile["name"]),
        (labels["phone"], profile["phone"] or "—"),
        (labels["state"], profile["state"]),
        (labels["district"], profile["district"]),
        (labels["taluk"], profile["taluk"] or "—"),
        (labels["village"], profile["village"]),
        (
            labels["land"],
            f"{profile['land_area']} {profile['land_unit']}",
        ),
        (labels["ownership"], profile["ownership"]),
        (labels["crop"], profile["crop"]),
        (labels["irrigation"], profile["irrigation"]),
        (labels["needs"], ", ".join(profile["needs"]) or "—"),
    ]

    for label, value in rows:
        left, right = st.columns([1, 2])
        with left:
            st.markdown(f"**{label}**")
        with right:
            st.write(value)


def render_farmer_profile():
    language = get_current_language()
    labels = PROFILE_TEXT.get(language, PROFILE_TEXT["en"])

    st.title(f"👨‍🌾 {t('profile')}")
    st.write(labels["intro"])

    saved_profile = st.session_state.get("farmer_profile", {})

    with st.form("farmer_profile_form"):
        st.markdown(f"### 👤 {labels['personal']}")

        name = st.text_input(
            labels["name"],
            value=saved_profile.get("name", ""),
            placeholder=labels["name"],
        )

        phone = st.text_input(
            labels["phone"],
            value=saved_profile.get("phone", ""),
            max_chars=10,
            placeholder="10-digit mobile number",
        )

        st.divider()
        st.markdown(f"### 📍 {labels['location']}")

        state = st.selectbox(
            labels["state"],
            options=[labels["karnataka"], "Other"],
            index=0 if saved_profile.get("state", labels["karnataka"]) == labels["karnataka"] else 1,
        )

        district_options = KARNATAKA_DISTRICTS + [labels["other"]]
        previous_district = saved_profile.get("district", "")
        district_index = (
            district_options.index(previous_district)
            if previous_district in district_options else 0
        )

        district = st.selectbox(
            labels["district"],
            options=district_options,
            index=district_index,
        )

        taluk = st.text_input(
            labels["taluk"],
            value=saved_profile.get("taluk", ""),
        )

        village = st.text_input(
            labels["village"],
            value=saved_profile.get("village", ""),
        )

        st.divider()
        st.markdown(f"### 🌾 {labels['farming']}")

        land_col, unit_col = st.columns(2)

        with land_col:
            land_area = st.number_input(
                labels["land"],
                min_value=0.0,
                max_value=10000.0,
                value=float(saved_profile.get("land_area", 0.0)),
                step=0.1,
            )

        unit_options = [labels["acres"], labels["hectares"]]
        previous_unit = saved_profile.get("land_unit", labels["acres"])

        with unit_col:
            land_unit = st.selectbox(
                labels["unit"],
                options=unit_options,
                index=unit_options.index(previous_unit)
                if previous_unit in unit_options else 0,
            )

        ownership_options = labels["ownership_options"]
        previous_ownership = saved_profile.get("ownership", ownership_options[0])

        ownership = st.selectbox(
            labels["ownership"],
            options=ownership_options,
            index=ownership_options.index(previous_ownership)
            if previous_ownership in ownership_options else 0,
        )

        crop_options = labels["crop_options"]
        previous_crop = saved_profile.get("crop", crop_options[0])

        crop = st.selectbox(
            labels["crop"],
            options=crop_options,
            index=crop_options.index(previous_crop)
            if previous_crop in crop_options else 0,
        )

        irrigation_options = labels["irrigation_options"]
        previous_irrigation = saved_profile.get(
            "irrigation", irrigation_options[0]
        )

        irrigation = st.selectbox(
            labels["irrigation"],
            options=irrigation_options,
            index=irrigation_options.index(previous_irrigation)
            if previous_irrigation in irrigation_options else 0,
        )

        needs = st.multiselect(
            labels["needs"],
            options=labels["need_options"],
            default=[
                item for item in saved_profile.get("needs", [])
                if item in labels["need_options"]
            ],
        )

        submitted = st.form_submit_button(
            f"💾 {labels['save']}",
            use_container_width=True,
            type="primary",
        )

    if submitted:
        if not name.strip() or not district.strip() or not village.strip():
            st.error(labels["required"])
        else:
            profile = {
                "name": name.strip(),
                "phone": phone.strip(),
                "state": state,
                "district": district,
                "taluk": taluk.strip(),
                "village": village.strip(),
                "land_area": land_area,
                "land_unit": land_unit,
                "ownership": ownership,
                "crop": crop,
                "irrigation": irrigation,
                "needs": needs,
            }

            st.session_state["farmer_profile"] = profile
            st.success(labels["saved"])
            saved_profile = profile

    if saved_profile:
        st.divider()
        _show_saved_profile(saved_profile, labels)
        st.caption(labels["edit"])
