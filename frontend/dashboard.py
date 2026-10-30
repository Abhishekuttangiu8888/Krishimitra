
import streamlit as st

from frontend.i18n import t
from frontend.components.cards import render_service_cards


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
        st.markdown(
            f"### 🎙️ {t('speak_now')}"
        )

        st.write(t("ask_question"))

        if st.button(
            f"🎤 {t('speak_now')}",
            type="primary",
            use_container_width=True,
            key="dashboard_voice_button",
        ):
            st.info(t("coming_soon"))

    render_service_cards()

    st.markdown(
        f'<div class="km-footer">{t("app_name")} · {t("tagline")}</div>',
        unsafe_allow_html=True,
    )
