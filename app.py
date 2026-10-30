
import streamlit as st

from frontend.auth_page import render_auth_page
from frontend.components.sidebar import render_sidebar
from frontend.profile_page import render_profile_page
from frontend.styles import apply_styles
from frontend.dashboard import render_dashboard
from frontend.mandi_page import render_mandi_page
from frontend.schemes_page import render_schemes_page


st.set_page_config(
    page_title="KRISHI MITRA",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Apply application-wide styling.
apply_styles()


# Authentication check.
if (
    not st.session_state.get("km_logged_in")
    or not st.session_state.get("km_token")
):
    render_auth_page()

else:
    # Render navigation sidebar.
    selected_page = render_sidebar()

    # Home dashboard.
    if selected_page == "Home":
        render_dashboard()

    # Mandi prices.
    elif selected_page == "Mandi Prices":
        render_mandi_page()

    # Government schemes.
    elif selected_page == "Government Schemes":
        render_schemes_page()

    # Crop disease detection.
    elif selected_page == "Crop Disease Detection":
        st.title("🌿 Crop Disease Detection")
        st.info(
            "Crop disease detection will be connected in "
            "a later development stage."
        )

    # Farmer profile.
    elif selected_page == "Profile":
        render_profile_page()

    else:
        st.warning("Please select a valid page from the sidebar.")
