import streamlit as st

from frontend.auth_page import render_auth_page
from frontend.components.sidebar import render_sidebar
from frontend.profile_page import render_profile_page

from frontend.styles import apply_styles
from frontend.dashboard import render_dashboard


st.set_page_config(
    page_title="KRISHI MITRA",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_styles()


if (
    not st.session_state.get("km_logged_in")
    or not st.session_state.get("km_token")
):

    render_auth_page()

else:

    selected_page = render_sidebar()

    if selected_page == "Profile":

        render_profile_page()

    elif selected_page == "Home":

        render_dashboard()

    elif selected_page == "Government Schemes":

        st.title("Government Schemes")

        st.info(
            "Scheme discovery will be connected "
            "in the next development stage."
        )

    elif selected_page == "Mandi Prices":

        st.title("Mandi Prices")

        st.info(
            "Verified mandi prices will be connected "
            "in the next development stage."
        )

    elif selected_page == "Crop Disease Detection":

        st.title("Crop Disease Detection")

        st.info(
            "Crop image analysis will be connected "
            "in the next development stage."
        )