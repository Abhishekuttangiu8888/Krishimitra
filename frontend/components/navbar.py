
import streamlit as st

from frontend.i18n import t


def render_navbar():
    st.markdown(
        f"""
        <div style="
            width: 100%;
            padding: 8px 4px 16px 4px;
            overflow: visible;
        ">
            <div class="km-brand">
                🌱 {t("app_name")}
            </div>
            <div class="km-tagline">
                {t("tagline")}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
