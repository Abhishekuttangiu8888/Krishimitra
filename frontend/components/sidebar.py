import streamlit as st


def render_sidebar():

    with st.sidebar:

        st.markdown("## 🌱 KRISHI MITRA")
        st.caption("Your agricultural companion")

        page = st.radio(
            "Navigation",
            options=[
                "Home",
                "Government Schemes",
                "Mandi Prices",
                "Crop Disease Detection",
                "Profile",
            ],
            index=0,
            label_visibility="collapsed",
            key="km_navigation",
        )

        st.divider()

        st.caption(
            f"Signed in: {st.session_state.get('km_mobile', '')}"
        )

        if st.button("Logout", use_container_width=True):

            for key in [
                "km_token",
                "km_mobile",
                "km_logged_in",
                "km_navigation",
            ]:
                st.session_state.pop(key, None)

            st.rerun()

        return page