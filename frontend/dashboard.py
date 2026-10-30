
import streamlit as st

from frontend.i18n import t
from frontend.components.cards import render_service_cards
from frontend.voice_interface import render_voice_interface


def render_dashboard():

    st.markdown(
        """
        <style>
        /* Floating chatbot position */
        .st-key-km_floating_chat {
            position: fixed !important;
            right: 24px !important;
            bottom: 24px !important;
            z-index: 999999 !important;

            width: 400px !important;
            max-width: calc(100vw - 32px) !important;
            max-height: min(650px, calc(100vh - 48px)) !important;

            overflow-y: auto !important;
            overflow-x: hidden !important;

            background: #ffffff !important;
            border: 2px solid #c8ddce !important;
            border-radius: 20px !important;

            box-shadow: 0 15px 45px rgba(0,0,0,0.22) !important;

            padding: 14px !important;
            box-sizing: border-box !important;
        }

        /* Closed launcher must have NO rectangle */
        .st-key-km_floating_chat:has(.st-key-km_open_chat) {
            width: auto !important;
            max-width: none !important;
            max-height: none !important;
            overflow: visible !important;
            padding: 0 !important;
            border: none !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
        }

        /* Open chat panel */
        .st-key-km_floating_chat h3 {
            color: #155b32 !important;
        }

        .st-key-km_floating_chat [data-testid="stChatMessage"] {
            background: #ffffff !important;
            border: 1px solid #e2eae3 !important;
            border-radius: 12px !important;
            padding: 10px !important;
        }

        @media (max-width: 600px) {
            .st-key-km_floating_chat {
                right: 10px !important;
                bottom: 10px !important;
                width: calc(100vw - 20px) !important;
                max-width: none !important;
                max-height: calc(100vh - 20px) !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="km-welcome">
            <h2>{t("welcome")}</h2>
            <p>{t("welcome_message")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_service_cards()

    st.markdown(
        f'<div class="km-footer">{t("app_name")} · {t("tagline")}</div>',
        unsafe_allow_html=True,
    )

    render_voice_interface()
