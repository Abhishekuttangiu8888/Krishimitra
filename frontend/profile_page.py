import requests
import streamlit as st


API_BASE = "http://127.0.0.1:8000/api"


def _headers():

    return {
        "Authorization": (
            f"Bearer {st.session_state.get('km_token', '')}"
        )
    }


def render_profile_page():

    st.title("👤 Profile")

    st.caption(
        "ನಿಮ್ಮ ವೈಯಕ್ತಿಕ ಮತ್ತು ಕೃಷಿ ಮಾಹಿತಿ · "
        "Your saved farmer information"
    )

    try:

        response = requests.get(
            f"{API_BASE}/farmer/profile",
            headers=_headers(),
            timeout=15,
        )

        response.raise_for_status()

        profile = response.json()

    except requests.RequestException:

        st.error(
            "Could not load your profile. "
            "Check that the backend is running and "
            "log in again if your session expired."
        )

        return

    with st.container(border=True):

        st.subheader(
            profile.get("full_name", "Farmer")
        )

        st.caption(
            f"Mobile: {st.session_state.get('km_mobile', '')}"
        )

        st.write(
            f"**Age:** {profile.get('age') or 'Not provided'}"
        )

        language = (
            "ಕನ್ನಡ"
            if profile.get("preferred_language") == "kn"
            else "English"
        )

        st.write(f"**Preferred language:** {language}")

    with st.container(border=True):

        st.subheader("Location")

        st.write(
            f"**State:** {profile.get('state') or '—'}"
        )

        st.write(
            f"**District:** {profile.get('district') or '—'}"
        )

        st.write(
            f"**Taluk:** {profile.get('taluk') or '—'}"
        )

        st.write(
            f"**Village:** {profile.get('village') or '—'}"
        )

    with st.container(border=True):

        st.subheader("Farm information")

        st.write(
            f"**Land area:** "
            f"{profile.get('land_area') or '—'} "
            f"{profile.get('land_unit') or ''}"
        )

        st.write(
            f"**Ownership:** "
            f"{profile.get('land_ownership') or '—'}"
        )

        st.write(
            f"**Crops:** "
            f"{', '.join(profile.get('crops') or []) or '—'}"
        )

        st.write(
            f"**Irrigation:** "
            f"{profile.get('irrigation_method') or '—'}"
        )

        st.write(
            f"**Farming type:** "
            f"{profile.get('farming_type') or '—'}"
        )

    with st.container(border=True):

        st.subheader("My farming needs")

        st.write(
            ", ".join(profile.get("needs") or [])
            or "Not provided"
        )

        st.write(
            profile.get("other_information") or ""
        )

    st.divider()

    with st.expander("Edit profile"):

        with st.form("edit_profile_form"):

            full_name = st.text_input(
                "Full name",
                value=profile.get("full_name") or "",
            )

            age = st.number_input(
                "Age",
                min_value=0,
                max_value=120,
                value=profile.get("age") or 0,
            )

            language = st.selectbox(
                "Preferred language",
                ["kn", "en"],
                index=(
                    0
                    if profile.get("preferred_language") == "kn"
                    else 1
                ),
            )

            state = st.text_input(
                "State",
                value=profile.get("state") or "Karnataka",
            )

            district = st.text_input(
                "District",
                value=profile.get("district") or "",
            )

            taluk = st.text_input(
                "Taluk",
                value=profile.get("taluk") or "",
            )

            village = st.text_input(
                "Village",
                value=profile.get("village") or "",
            )

            land_area = st.text_input(
                "Land area",
                value=profile.get("land_area") or "",
            )

            units = [
                "acres",
                "hectares",
                "gunta",
            ]

            current_unit = profile.get("land_unit")

            land_unit = st.selectbox(
                "Unit",
                units,
                index=(
                    units.index(current_unit)
                    if current_unit in units
                    else 0
                ),
            )

            ownerships = [
                "",
                "Owner",
                "Tenant",
                "Shared / leased",
                "Other",
            ]

            current_ownership = profile.get("land_ownership")

            ownership = st.selectbox(
                "Ownership",
                ownerships,
                index=(
                    ownerships.index(current_ownership)
                    if current_ownership in ownerships
                    else 0
                ),
            )

            crop_options = [
                "Paddy",
                "Ragi",
                "Maize",
                "Sugarcane",
                "Cotton",
                "Groundnut",
                "Arecanut",
                "Coconut",
                "Tur / Pigeon pea",
                "Other",
            ]

            crops = st.multiselect(
                "Main crops",
                crop_options,
                default=[
                    item
                    for item in profile.get("crops", [])
                    if item in crop_options
                ],
            )

            irrigation_options = [
                "",
                "Rain-fed",
                "Canal",
                "Borewell",
                "Open well",
                "Drip",
                "Sprinkler",
                "Other",
            ]

            current_irrigation = profile.get("irrigation_method")

            irrigation = st.selectbox(
                "Irrigation",
                irrigation_options,
                index=(
                    irrigation_options.index(current_irrigation)
                    if current_irrigation in irrigation_options
                    else 0
                ),
            )

            farming_options = [
                "",
                "Conventional",
                "Organic",
                "Natural farming",
                "Mixed farming",
                "Other",
            ]

            current_farming = profile.get("farming_type")

            farming = st.selectbox(
                "Farming type",
                farming_options,
                index=(
                    farming_options.index(current_farming)
                    if current_farming in farming_options
                    else 0
                ),
            )

            need_options = [
                "Government schemes",
                "Crop disease help",
                "Mandi prices",
                "Weather information",
                "Soil health",
                "Crop planning",
                "Market / transport information",
            ]

            needs = st.multiselect(
                "Farming needs",
                need_options,
                default=[
                    item
                    for item in profile.get("needs", [])
                    if item in need_options
                ],
            )

            other = st.text_area(
                "Other information",
                value=profile.get("other_information") or "",
            )

            save = st.form_submit_button(
                "Save changes",
                type="primary",
            )

        if save:

            payload = {
                "full_name": full_name,
                "age": age or None,
                "preferred_language": language,
                "state": state or "Karnataka",
                "district": district or None,
                "taluk": taluk or None,
                "village": village or None,
                "land_area": land_area or None,
                "land_unit": land_unit,
                "land_ownership": ownership or None,
                "crops": crops,
                "irrigation_method": irrigation or None,
                "farming_type": farming or None,
                "needs": needs,
                "other_information": other or None,
            }

            try:

                saved = requests.put(
                    f"{API_BASE}/farmer/profile",
                    json=payload,
                    headers=_headers(),
                    timeout=15,
                )

                saved.raise_for_status()

                st.success(
                    "Profile updated successfully."
                )

                st.rerun()

            except requests.RequestException as exc:

                try:

                    st.error(
                        exc.response.json().get(
                            "detail",
                            "Could not update profile.",
                        )
                    )

                except Exception:

                    st.error(
                        "Could not connect to the backend."
                    )