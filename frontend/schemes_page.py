
import streamlit as st
import requests


API_BASE = "http://127.0.0.1:8000/api"


# ---------------------------------------------------------
# GOVERNMENT SCHEME INFORMATION
# ---------------------------------------------------------

SCHEMES = [
    {
        "id": "pmkisan",
        "name": "PM-KISAN",
        "kannada": "ಪ್ರಧಾನ ಮಂತ್ರಿ ಕಿಸಾನ್ ಸಮ್ಮಾನ್ ನಿಧಿ",
        "category": "Income Support",
        "benefit": (
            "Eligible farmer families receive ₹6,000 per year "
            "in three instalments of ₹2,000 each."
        ),
        "benefit_kn": (
            "ಅರ್ಹ ರೈತ ಕುಟುಂಬಗಳಿಗೆ ವರ್ಷಕ್ಕೆ ₹6,000 "
            "ಮೂರು ಕಂತುಗಳಲ್ಲಿ ನೀಡಲಾಗುತ್ತದೆ."
        ),
        "eligibility": (
            "Landholding farmer families, subject to official "
            "exclusion criteria and verification."
        ),
        "eligibility_kn": (
            "ಅಧಿಕೃತ ಹೊರಗಿಡುವ ನಿಯಮಗಳು ಮತ್ತು ಪರಿಶೀಲನೆಗೆ ಒಳಪಟ್ಟು "
            "ಭೂಮಿ ಹೊಂದಿರುವ ರೈತ ಕುಟುಂಬಗಳು."
        ),
        "documents": [
            "Aadhaar details",
            "Bank account details",
            "Landholding records",
        ],
        "url": "https://pmkisan.gov.in/",
        "source": "Government of India – PM-KISAN",
    },
    {
        "id": "pmfby",
        "name": "Pradhan Mantri Fasal Bima Yojana",
        "kannada": "ಪ್ರಧಾನ ಮಂತ್ರಿ ಫಸಲ್ ಬಿಮಾ ಯೋಜನೆ",
        "category": "Crop Insurance",
        "benefit": (
            "Crop insurance against specified crop-loss risks, "
            "subject to notified crops, areas and season rules."
        ),
        "benefit_kn": (
            "ಅಧಿಸೂಚಿತ ಬೆಳೆಗಳು, ಪ್ರದೇಶಗಳು ಮತ್ತು ಋತುವಿನ ನಿಯಮಗಳಿಗೆ "
            "ಒಳಪಟ್ಟು ಬೆಳೆ ನಷ್ಟದ ವಿರುದ್ಧ ವಿಮಾ ರಕ್ಷಣೆ."
        ),
        "eligibility": (
            "Farmers with an insurable interest in notified crops "
            "grown in notified areas during the relevant season."
        ),
        "eligibility_kn": (
            "ಸಂಬಂಧಿತ ಋತುವಿನಲ್ಲಿ ಅಧಿಸೂಚಿತ ಪ್ರದೇಶದಲ್ಲಿ ಅಧಿಸೂಚಿತ "
            "ಬೆಳೆ ಬೆಳೆಯುವ ವಿಮಾ ಹಿತಾಸಕ್ತಿ ಹೊಂದಿರುವ ರೈತರು."
        ),
        "documents": [
            "Identity proof",
            "Bank account details",
            "Land or cultivation records",
            "Crop and sowing details",
        ],
        "url": "https://pmfby.gov.in/",
        "source": "Government of India – PMFBY",
    },
    {
        "id": "kcc",
        "name": "Kisan Credit Card",
        "kannada": "ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್",
        "category": "Agricultural Credit",
        "benefit": (
            "Institutional credit for cultivation, post-harvest "
            "expenses and eligible allied agricultural activities."
        ),
        "benefit_kn": (
            "ಕೃಷಿ ಚಟುವಟಿಕೆಗಳು, ಕೊಯ್ಲಿನ ನಂತರದ ವೆಚ್ಚಗಳು ಮತ್ತು "
            "ಅರ್ಹ ಕೃಷಿ ಸಂಬಂಧಿತ ಚಟುವಟಿಕೆಗಳಿಗೆ ಸಾಲ ಸೌಲಭ್ಯ."
        ),
        "eligibility": (
            "Owner cultivators, tenant farmers, oral lessees, "
            "sharecroppers and eligible farmer groups."
        ),
        "eligibility_kn": (
            "ಸ್ವಂತ ಜಮೀನಿನಲ್ಲಿ ಕೃಷಿ ಮಾಡುವವರು, ಗೇಣಿದಾರರು, "
            "ಹಂಚಿಕೆದಾರರು ಮತ್ತು ಅರ್ಹ ರೈತ ಗುಂಪುಗಳು."
        ),
        "documents": [
            "Identity and address proof",
            "Land or cultivation details",
            "Crop and acreage details",
            "Bank-required documents",
        ],
        "url": "https://fasalrin.gov.in/",
        "source": "Government of India – Kisan Credit Card",
    },
]


# ---------------------------------------------------------
# API HELPERS
# ---------------------------------------------------------

def get_auth_headers():

    token = st.session_state.get("km_token")

    if not token:
        return None

    return {
        "Authorization": f"Bearer {token}"
    }


def get_saved_farmer_profile():

    headers = get_auth_headers()

    if not headers:
        st.error("Please log in again.")
        return None

    try:
        response = requests.get(
            f"{API_BASE}/farmer/profile",
            headers=headers,
            timeout=20,
        )

        response.raise_for_status()

        data = response.json()

        profile = data.get(
            "profile",
            data.get("data", data),
        )

        if not isinstance(profile, dict):
            st.error("Invalid farmer profile response.")
            return None

        return profile

    except requests.RequestException as error:

        st.error(
            "Unable to load your saved farmer profile. "
            f"Details: {error}"
        )

        return None

    except ValueError:

        st.error("The profile API returned invalid JSON.")
        return None


def transcribe_crop_audio(audio_file):

    headers = get_auth_headers()

    if not headers:
        st.error("Please log in again.")
        return None

    try:
        response = requests.post(
            f"{API_BASE}/voice/transcribe",
            headers=headers,
            files={
                "audio": (
                    audio_file.name,
                    audio_file.getvalue(),
                    audio_file.type or "audio/wav",
                )
            },
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()

        text = (
            data.get("text")
            or data.get("transcription")
            or data.get("transcript")
        )

        if not text:
            st.error(
                "Speech was not recognized. Please try again "
                "or type the crop name."
            )
            return None

        return text.strip()

    except requests.RequestException as error:

        st.error(f"Voice transcription failed: {error}")
        return None

    except ValueError:

        st.error("The voice API returned invalid JSON.")
        return None


# ---------------------------------------------------------
# PROFILE HELPERS
# ---------------------------------------------------------

def get_profile_value(profile, *keys):

    for key in keys:

        value = profile.get(key)

        if value not in (None, ""):
            return value

    return "Not available"


def display_saved_profile(profile, kannada=False):

    district = get_profile_value(
        profile,
        "district",
        "district_name",
    )

    village = get_profile_value(
        profile,
        "village",
        "village_name",
    )

    land_area = get_profile_value(
        profile,
        "land_area",
        "total_land",
        "land_size",
    )

    st.markdown(
        "### ನಿಮ್ಮ ಉಳಿಸಿದ ರೈತ ವಿವರಗಳು"
        if kannada
        else "### Your saved farmer details"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "ಜಿಲ್ಲೆ" if kannada else "District",
        str(district),
    )

    col2.metric(
        "ಗ್ರಾಮ" if kannada else "Village",
        str(village),
    )

    col3.metric(
        "ಭೂಮಿ" if kannada else "Land area",
        str(land_area),
    )


# ---------------------------------------------------------
# PRELIMINARY SCHEME MATCHING
# ---------------------------------------------------------

def check_farmer_scheme_relevance(profile, crop):

    results = []

    ownership = str(
        get_profile_value(
            profile,
            "land_ownership",
            "ownership",
        )
    ).lower()

    land_area = get_profile_value(
        profile,
        "land_area",
        "total_land",
        "land_size",
    )

    farming_type = str(
        get_profile_value(
            profile,
            "farming_type",
            "farmer_type",
        )
    ).lower()

    # PM-KISAN: preliminary landholding indicator only.
    if (
        land_area != "Not available"
        and any(word in ownership for word in [
            "owner",
            "owned",
            "self",
            "ಸ್ವಂತ",
        ])
    ):

        results.append({
            "scheme_id": "pmkisan",
            "reason": (
                "Your saved profile indicates land ownership. "
                "Check the official PM-KISAN exclusion criteria "
                "before determining eligibility."
            ),
            "reason_kn": (
                "ನಿಮ್ಮ ಪ್ರೊಫೈಲ್‌ನಲ್ಲಿ ಭೂಮಿ ಮಾಲೀಕತ್ವದ ಮಾಹಿತಿ ಇದೆ. "
                "ಅಧಿಕೃತ PM-KISAN ನಿಯಮಗಳನ್ನು ಪರಿಶೀಲಿಸಿ."
            ),
        })

    # KCC: preliminary farming-status indicator.
    if (
        ownership != "not available"
        or farming_type
    ):

        results.append({
            "scheme_id": "kcc",
            "reason": (
                "Your farming profile may be relevant for Kisan "
                "Credit Card. The bank must assess the application."
            ),
            "reason_kn": (
                "ನಿಮ್ಮ ಕೃಷಿ ವಿವರಗಳು ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್‌ಗೆ "
                "ಸಂಬಂಧಿಸಿರಬಹುದು. ಬ್ಯಾಂಕ್ ಅಂತಿಮ ಪರಿಶೀಲನೆ ಮಾಡುತ್ತದೆ."
            ),
        })

    # PMFBY: crop and notified location must be verified.
    results.append({
        "scheme_id": "pmfby",
        "reason": (
            f"You entered {crop}. Verify whether this crop and "
            "your district are notified for the current season."
        ),
        "reason_kn": (
            f"ನೀವು {crop} ಬೆಳೆಯನ್ನು ನಮೂದಿಸಿದ್ದೀರಿ. "
            "ಈ ಋತುವಿನಲ್ಲಿ ನಿಮ್ಮ ಜಿಲ್ಲೆ ಮತ್ತು ಬೆಳೆ ಅಧಿಸೂಚಿತವಾಗಿದೆಯೇ "
            "ಎಂದು ಪರಿಶೀಲಿಸಿ."
        ),
    })

    return results


# ---------------------------------------------------------
# DISPLAY SCHEME DETAILS
# ---------------------------------------------------------

def render_scheme_card(scheme, kannada=False, reason=None):

    name = (
        scheme["kannada"]
        if kannada
        else scheme["name"]
    )

    benefit = (
        scheme["benefit_kn"]
        if kannada
        else scheme["benefit"]
    )

    eligibility = (
        scheme["eligibility_kn"]
        if kannada
        else scheme["eligibility"]
    )

    with st.container(border=True):

        st.markdown(f"### 🌾 {name}")

        st.write(benefit)

        if reason:

            st.info(
                reason["reason_kn"]
                if kannada
                else reason["reason"]
            )

        with st.expander(
            "ಹೆಚ್ಚಿನ ಮಾಹಿತಿ"
            if kannada
            else "View scheme details"
        ):

            st.markdown(
                "**ಅರ್ಹತೆ**"
                if kannada
                else "**Eligibility**"
            )

            st.write(eligibility)

            st.markdown(
                "**ಅಗತ್ಯ ದಾಖಲೆಗಳು**"
                if kannada
                else "**Documents generally required**"
            )

            for document in scheme["documents"]:
                st.write(f"• {document}")

            st.caption(
                f"Source: {scheme['source']}"
            )

            st.link_button(
                "ಅಧಿಕೃತ ವೆಬ್‌ಸೈಟ್ ತೆರೆಯಿರಿ"
                if kannada
                else "Visit official website",
                scheme["url"],
                use_container_width=True,
            )


# ---------------------------------------------------------
# FARMER ELIGIBILITY SECTION
# ---------------------------------------------------------

def render_eligibility_section(kannada=False):

    st.markdown(
        "## ನಿಮ್ಮ ಪ್ರಸ್ತುತ ಬೆಳೆಗೆ ಯೋಜನೆಗಳನ್ನು ಪರಿಶೀಲಿಸಿ"
        if kannada
        else "## Find schemes for your current crop"
    )

    st.write(
        "ನಿಮ್ಮ ಹಿಂದಿನ ರೈತ ವಿವರಗಳನ್ನು ಬಳಸುತ್ತೇವೆ. "
        "ಈಗ ನೀವು ಬೆಳೆಯುತ್ತಿರುವ ಬೆಳೆಯನ್ನು ಮಾತ್ರ ನಮೂದಿಸಿ."
        if kannada
        else "We will reuse your saved farmer profile. "
             "You only need to tell us which crop you are "
             "currently growing."
    )

    profile = get_saved_farmer_profile()

    if not profile:

        st.warning(
            "ನಿಮ್ಮ ಉಳಿಸಿದ ರೈತ ಪ್ರೊಫೈಲ್ ಲಭ್ಯವಿಲ್ಲ."
            if kannada
            else "Your saved farmer profile could not be loaded."
        )

        return

    display_saved_profile(profile, kannada)

    st.divider()

    st.markdown(
        "**ಈಗ ಬೆಳೆಯುತ್ತಿರುವ ಬೆಳೆ ಯಾವುದು?**"
        if kannada
        else "**Which crop are you growing now?**"
    )

    audio_file = st.audio_input(
        "ನಿಮ್ಮ ಬೆಳೆಯ ಹೆಸರನ್ನು ಹೇಳಿ"
        if kannada
        else "Speak your crop name",
        key="schemes_crop_audio",
    )

    if audio_file:

        if st.button(
            "ಧ್ವನಿಯನ್ನು ಗುರುತಿಸಿ"
            if kannada
            else "Recognize voice",
            key="schemes_transcribe_crop",
        ):

            recognized_crop = transcribe_crop_audio(
                audio_file
            )

            if recognized_crop:

                st.session_state[
                    "schemes_crop_input"
                ] = recognized_crop

                st.rerun()

    crop = st.text_input(
        "ಬೆಳೆ ಹೆಸರು"
        if kannada
        else "Crop name",
        placeholder=(
            "ಉದಾ: ರಾಗಿ, ಭತ್ತ, ಜೋಳ"
            if kannada
            else "Example: Ragi, Paddy, Maize"
        ),
        key="schemes_crop_input",
    ).strip()

    if st.button(
        "ಅರ್ಹತೆ ಪರಿಶೀಲಿಸಿ"
        if kannada
        else "Check scheme relevance",
        type="primary",
        use_container_width=True,
        key="schemes_check_eligibility",
    ):

        if not crop:

            st.warning(
                "ದಯವಿಟ್ಟು ಬೆಳೆಯ ಹೆಸರನ್ನು ನಮೂದಿಸಿ."
                if kannada
                else "Please enter your crop name."
            )

            return

        results = check_farmer_scheme_relevance(
            profile,
            crop,
        )

        st.session_state["schemes_results"] = results
        st.session_state["schemes_last_crop"] = crop

    # Display previously generated results.
    results = st.session_state.get(
        "schemes_results"
    )

    if results:

        last_crop = st.session_state.get(
            "schemes_last_crop",
            "",
        )

        st.divider()

        st.markdown(
            "### ನಿಮಗೆ ಸಂಬಂಧಿಸಬಹುದಾದ ಯೋಜನೆಗಳು"
            if kannada
            else "### Schemes that may be relevant to you"
        )

        st.write(
            (
                f"ಬೆಳೆ: {last_crop}"
                if kannada
                else f"Current crop: {last_crop}"
            )
        )

        result_map = {
            item["scheme_id"]: item
            for item in results
        }

        for scheme in SCHEMES:

            reason = result_map.get(
                scheme["id"]
            )

            if reason:

                render_scheme_card(
                    scheme,
                    kannada,
                    reason,
                )

        


# ---------------------------------------------------------
# MAIN GOVERNMENT SCHEMES PAGE
# ---------------------------------------------------------

def render_schemes_page():

    st.markdown(
        """
        <style>
        .schemes-header {
            background: linear-gradient(120deg, #e9f7ed, #f6fbf6);
            padding: 25px;
            border-radius: 16px;
            border-left: 5px solid #238447;
            margin-bottom: 20px;
        }

        .schemes-header h2 {
            color: #155b32;
            margin-bottom: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    language = st.radio(
        "Language / ಭಾಷೆ",
        ["ಕನ್ನಡ", "English"],
        horizontal=True,
        key="schemes_language",
    )

    kannada = language == "ಕನ್ನಡ"

    st.markdown(
        f"""
        <div class="schemes-header">
            <h2>
                {"🏛️ ಸರ್ಕಾರಿ ಕೃಷಿ ಯೋಜನೆಗಳು" if kannada else "🏛️ Government Schemes"}
            </h2>
            <p>
                {
                    "ನಿಮ್ಮ ಕೃಷಿಗೆ ಸಂಬಂಧಿಸಿದ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಿ."
                    if kannada
                    else "Discover government support available for farmers."
                }
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_eligibility_section(kannada)

    st.divider()

    st.markdown(
        "## ಎಲ್ಲಾ ಯೋಜನೆಗಳು"
        if kannada
        else "## Browse all schemes"
    )

    categories = ["All"] + sorted(
        {
            scheme["category"]
            for scheme in SCHEMES
        }
    )

    selected_category = st.selectbox(
        "ವರ್ಗ ಆಯ್ಕೆಮಾಡಿ"
        if kannada
        else "Filter by category",
        categories,
        format_func=lambda value: (
            "ಎಲ್ಲಾ ಯೋಜನೆಗಳು"
            if kannada and value == "All"
            else value
        ),
    )

    search = st.text_input(
        "ಯೋಜನೆ ಹುಡುಕಿ"
        if kannada
        else "Search schemes",
        placeholder=(
            "ಯೋಜನೆಯ ಹೆಸರು ನಮೂದಿಸಿ"
            if kannada
            else "Search by scheme name"
        ),
    ).strip().lower()

    filtered_schemes = []

    for scheme in SCHEMES:

        matches_category = (
            selected_category == "All"
            or scheme["category"] == selected_category
        )

        searchable = (
            scheme["name"]
            + " "
            + scheme["kannada"]
            + " "
            + scheme["category"]
            + " "
            + scheme["benefit"]
        ).lower()

        matches_search = (
            not search
            or search in searchable
        )

        if matches_category and matches_search:
            filtered_schemes.append(scheme)

    st.caption(
        f"{len(filtered_schemes)} "
        + (
            "ಯೋಜನೆಗಳು ಕಂಡುಬಂದಿವೆ"
            if kannada
            else "schemes found"
        )
    )

    if not filtered_schemes:

        st.info(
            "ಯಾವುದೇ ಯೋಜನೆ ಕಂಡುಬಂದಿಲ್ಲ."
            if kannada
            else "No matching schemes found."
        )

    else:

        columns = st.columns(2)

        for index, scheme in enumerate(
            filtered_schemes
        ):

            with columns[index % 2]:

                render_scheme_card(
                    scheme,
                    kannada,
                )

    st.divider()

    st.caption(
        "ಅರ್ಜಿ ಸಲ್ಲಿಸುವ ಮೊದಲು ಅಧಿಕೃತ ಸರ್ಕಾರಿ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ "
        "ಪ್ರಸ್ತುತ ನಿಯಮಗಳು ಮತ್ತು ಅರ್ಹತೆಯನ್ನು ಪರಿಶೀಲಿಸಿ."
        if kannada
        else "Before applying, verify current eligibility, "
             "deadlines and requirements on the official "
             "government portal."
    )
