import base64
from pathlib import Path

import requests
import streamlit as st

from frontend.i18n import t, get_current_language


CHAT_API_URL = "http://127.0.0.1:8000/api/chat/message"
TRANSCRIBE_API_URL = "http://127.0.0.1:8000/api/voice/transcribe"

AVATAR_PATH = (
    Path(__file__).parent
    / "assets"
    / "krishi_farmer_avatar.png"
)


def initialize_chat():
    if "km_chat_history" not in st.session_state:
        st.session_state.km_chat_history = []

    if "km_chat_open" not in st.session_state:
        st.session_state.km_chat_open = False


def load_avatar():
    if not AVATAR_PATH.exists():
        return None

    return base64.b64encode(
        AVATAR_PATH.read_bytes()
    ).decode("utf-8")


def clear_chat():
    st.session_state.km_chat_history = []
    st.rerun()


def transcribe_audio(audio_file):
    language = get_current_language()

    try:
        response = requests.post(
            TRANSCRIBE_API_URL,
            files={
                "audio": (
                    "voice_message.wav",
                    audio_file.getvalue(),
                    "audio/wav",
                )
            },
            data={
                "language": language,
            },
            timeout=60,
        )

        response.raise_for_status()

        transcript = response.json().get("text", "").strip()

        if not transcript:
            st.error(t("voice_not_recognized"))
            return None

        return transcript

    except requests.exceptions.RequestException:
        st.error(t("voice_service_error"))

    except Exception:
        st.error(t("voice_error"))

    return None


def send_message(message):
    history = st.session_state.km_chat_history[-12:]
    language = get_current_language()

    try:
        response = requests.post(
            CHAT_API_URL,
            json={
                "message": message,
                "history": history,
                "language": language,
            },
            timeout=90,
        )

        response.raise_for_status()
        result = response.json()

        reply = result.get("reply", "").strip()

        if not result.get("success") or not reply:
            st.error(t("answer_unavailable"))
            return False

        st.session_state.km_chat_history.extend([
            {
                "role": "user",
                "content": message,
            },
            {
                "role": "assistant",
                "content": reply,
            },
        ])

        return True

    except requests.exceptions.ConnectionError:
        st.error(t("backend_not_running"))

    except requests.exceptions.Timeout:
        st.error(t("chat_timeout"))

    except requests.exceptions.HTTPError as error:
        try:
            detail = response.json().get("detail", str(error))
        except Exception:
            detail = str(error)

        st.error(f"{t('chat_api_error')}: {detail}")

    except Exception as error:
        st.error(f"{t('general_error')}: {error}")

    return False


def render_voice_interface():
    initialize_chat()

    avatar_base64 = load_avatar()

    if avatar_base64:
        launcher_image = (
            f"data:image/png;base64,{avatar_base64}"
        )

        launcher_css = f"""
        <style>
        .st-key-km_floating_chat:has(.st-key-km_open_chat) {{
            width: auto !important;
            max-width: none !important;
            max-height: none !important;
            overflow: visible !important;
            padding: 0 !important;
            border: none !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
        }}

        .st-key-km_floating_chat .st-key-km_open_chat {{
            width: 82px !important;
            height: 82px !important;
            position: relative !important;
            overflow: visible !important;
        }}

        .st-key-km_floating_chat .st-key-km_open_chat button {{
            width: 76px !important;
            height: 76px !important;
            min-height: 76px !important;
            padding: 0 !important;

            border-radius: 50% !important;
            border: 3px solid #ffffff !important;

            background-color: #176b3a !important;
            background-image: url("{launcher_image}") !important;
            background-size: cover !important;
            background-position: center 35% !important;
            background-repeat: no-repeat !important;

            box-shadow: 0 5px 22px rgba(0, 0, 0, 0.25) !important;

            font-size: 0 !important;
            transition: transform 0.2s ease !important;
        }}

        .st-key-km_floating_chat .st-key-km_open_chat button:hover {{
            transform: scale(1.07) !important;
            border-color: #a9df83 !important;
        }}

        .st-key-km_floating_chat .st-key-km_open_chat button::after {{
            content: "" !important;
            position: absolute !important;
            right: 0 !important;
            bottom: 0 !important;

            width: 15px !important;
            height: 15px !important;

            background: #20c66b !important;
            border: 3px solid #ffffff !important;
            border-radius: 50% !important;
        }}

        .st-key-km_floating_chat .st-key-km_open_chat button:hover::before {{
            content: "{t('chat_with_krishi_mitra')}" !important;
            position: absolute !important;
            right: 88px !important;
            top: 18px !important;

            width: max-content !important;
            padding: 10px 15px !important;

            background: #145b35 !important;
            color: #ffffff !important;

            border-radius: 10px !important;
            font-size: 13px !important;
            font-weight: 600 !important;

            box-shadow: 0 4px 14px rgba(0,0,0,0.2) !important;
            z-index: 999999 !important;
        }}
        </style>
        """

    else:
        launcher_css = """
        <style>
        .st-key-km_floating_chat:has(.st-key-km_open_chat) {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
        }
        </style>
        """

    st.markdown(
        launcher_css,
        unsafe_allow_html=True,
    )

    with st.container(key="km_floating_chat"):

        if not st.session_state.km_chat_open:

            if st.button(
                " ",
                key="km_open_chat",
                help=t("chat_with_krishi_mitra"),
                type="primary",
            ):
                st.session_state.km_chat_open = True
                st.rerun()

        else:

            with st.container(border=True):

                title_col, close_col = st.columns([5, 1])

                with title_col:
                    st.markdown(
                        f"### 🌱 {t('app_name')}"
                    )

                with close_col:
                    if st.button(
                        "✕",
                        key="km_close_chat",
                        help=t("close"),
                    ):
                        st.session_state.km_chat_open = False
                        st.rerun()

                st.caption(t("chat_instructions"))

                if st.button(
                    f"🗑️ {t('clear_conversation')}",
                    key="km_clear_chat",
                ):
                    clear_chat()

                with st.container(height=300):

                    if not st.session_state.km_chat_history:
                        st.markdown(
                            t("chat_greeting")
                        )

                    for message in st.session_state.km_chat_history:

                        with st.chat_message(
                            message["role"],
                            avatar=(
                                "🌱"
                                if message["role"] == "assistant"
                                else "👨‍🌾"
                            ),
                        ):
                            st.markdown(message["content"])

                prompt = st.chat_input(
                    t("chat_input_placeholder"),
                    accept_audio=True,
                    audio_sample_rate=16000,
                    key="km_floating_chat_input",
                )

                if prompt is not None:

                    user_message = (
                        prompt.text or ""
                    ).strip()

                    if prompt.audio is not None:

                        with st.spinner(
                            t("recognizing_voice")
                        ):
                            transcript = transcribe_audio(
                                prompt.audio
                            )

                        if transcript:
                            user_message = transcript

                            st.info(
                                f"{t('you_said')}: {transcript}"
                            )

                    if user_message:

                        with st.spinner(
                            t("assistant_responding")
                        ):
                            send_message(user_message)

                        st.rerun()