
import streamlit as st

from frontend.i18n import t
from frontend.components.cards import render_service_cards
from frontend.voice_interface import render_voice_interface


def render_dashboard():

    st.markdown(
        f"""
        <div class="km-welcome">
            <h2>{t("welcome")}</h2>
            <p>{t("welcome_message")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="km-section-label">{t("voice_assistant")}</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        render_voice_interface()

    render_service_cards()

    st.markdown(
        f'<div class="km-footer">{t("app_name")} · {t("tagline")}</div>',
        unsafe_allow_html=True,
    )
