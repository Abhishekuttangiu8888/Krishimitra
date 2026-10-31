
import streamlit as st

from frontend.i18n import (
    t,
    get_current_language,
    get_language_name,
    set_language,
    SUPPORTED_LANGUAGES,
)


# --------------------------------------------------
# LANGUAGE CHANGE
# --------------------------------------------------

def change_language():

    selected_language = st.session_state.get("km_language_selector")

    if selected_language in SUPPORTED_LANGUAGES:
        set_language(selected_language)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

def render_sidebar():

    with st.sidebar:

        # ------------------------------------------
        # BRAND
        # ------------------------------------------

        st.markdown(f"## 🌱 {t('app_name')}")
        st.caption(t("app_tagline"))

        st.divider()

        # ------------------------------------------
        # LANGUAGE SELECTOR
        # ------------------------------------------

        st.markdown(f"### 🌐 {t('language')}")

        current_language = get_current_language()

        if "km_language_selector" not in st.session_state:
            st.session_state.km_language_selector = current_language

        st.selectbox(
            label=t("select_language"),
            options=list(SUPPORTED_LANGUAGES.keys()),
            format_func=get_language_name,
            index=list(SUPPORTED_LANGUAGES.keys()).index(current_language),
            key="km_language_selector",
            on_change=change_language,
            label_visibility="collapsed",
        )

        st.divider()

        # ------------------------------------------
        # NAVIGATION
        # ------------------------------------------

        pages = {
            t("home"): "Home",
            t("government_schemes"): "Government Schemes",
            t("mandi_prices"): "Mandi Prices",
            t("crop_disease_detection"): "Crop Disease Detection",
            t("profile"): "Profile",
        }

        selected_label = st.radio(
            t("navigation"),
            options=list(pages.keys()),
            index=0,
            label_visibility="collapsed",
            key="km_navigation",
        )

        selected_page = pages[selected_label]

        st.divider()

        # ------------------------------------------
        # USER INFORMATION
        # ------------------------------------------

        st.caption(
            f"{t('signed_in')}: "
            f"{st.session_state.get('km_mobile', '')}"
        )

        # ------------------------------------------
        # LOGOUT
        # ------------------------------------------

        if st.button(
            t("logout"),
            use_container_width=True,
        ):

            for key in [
                "km_token",
                "km_mobile",
                "km_logged_in",
                "km_navigation",
                "km_language_selector",
            ]:
                st.session_state.pop(key, None)

            st.rerun()

        return selected_page
