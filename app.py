
import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="KRISHI MITRA",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# IMPORTS
# --------------------------------------------------

from frontend.auth_page import render_auth_page
from frontend.components.sidebar import render_sidebar

from frontend.styles import apply_styles

from frontend.dashboard import render_dashboard
from frontend.mandi_page import render_mandi_page
from frontend.schemes_page import render_schemes_page
from frontend.disease_page import render_disease_page
from frontend.profile_page import render_profile_page


# --------------------------------------------------
# APPLY APPLICATION STYLES
# --------------------------------------------------

apply_styles()


# --------------------------------------------------
# SESSION STATE INITIALIZATION
# --------------------------------------------------

if "km_logged_in" not in st.session_state:
    st.session_state["km_logged_in"] = False

if "km_token" not in st.session_state:
    st.session_state["km_token"] = None


# --------------------------------------------------
# AUTHENTICATION
# --------------------------------------------------

if not st.session_state.get("km_logged_in") or not st.session_state.get("km_token"):

    render_auth_page()

    st.stop()


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

selected_page = render_sidebar()


# --------------------------------------------------
# PAGE ROUTING
# --------------------------------------------------

if selected_page == "Home":

    render_dashboard()


elif selected_page == "Mandi Prices":

    render_mandi_page()


elif selected_page == "Government Schemes":

    render_schemes_page()


elif selected_page == "Crop Disease Detection":

    render_disease_page()


elif selected_page == "Profile":

    render_profile_page()


else:

    st.warning("Please select a valid page from the sidebar.")
