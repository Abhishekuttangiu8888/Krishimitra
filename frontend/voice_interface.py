
import base64
from pathlib import Path

import requests
import streamlit as st


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
            timeout=60,
        )

        response.raise_for_status()

        transcript = response.json().get("text", "").strip()

        if not transcript:
            st.error("ಧ್ವನಿ ಗುರುತಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ.")
            return None

        return transcript

    except requests.exceptions.RequestException as error:
        st.error(f"Voice service error: {error}")
    except Exception as error:
        st.error(f"Voice error: {error}")

    return None


def send_message(message):
    history = st.session_state.km_chat_history[-12:]

    try:
        response = requests.post(
            CHAT_API_URL,
            json={
                "message": message,
                "history": history,
            },
            timeout=90,
        )

        response.raise_for_status()
        result = response.json()

        reply = result.get("reply", "").strip()

        if not result.get("success") or not reply:
            st.error("ಉತ್ತರ ಪಡೆಯಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ.")
            return False

        st.session_state.km_chat_history.extend([
            {"role": "user", "content": message},
            {"role": "assistant", "content": reply},
        ])

        return True

    except requests.exceptions.ConnectionError:
        st.error("KRISHI MITRA backend ಚಾಲನೆಯಲ್ಲಿದೆಯೇ ಪರಿಶೀಲಿಸಿ.")
    except requests.exceptions.Timeout:
        st.error("ಉತ್ತರ ಪಡೆಯಲು ಹೆಚ್ಚು ಸಮಯ ತೆಗೆದುಕೊಳ್ಳುತ್ತಿದೆ.")
    except requests.exceptions.HTTPError as error:
        try:
            detail = response.json().get("detail", str(error))
        except Exception:
            detail = str(error)

        st.error(f"Chat API error: {detail}")

    except Exception as error:
        st.error(f"Error: {error}")

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
            content: "Chat with KRISHI MITRA" !important;
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

    st.markdown(launcher_css, unsafe_allow_html=True)

    with st.container(key="km_floating_chat"):

        if not st.session_state.km_chat_open:

            if st.button(
                " ",
                key="km_open_chat",
                help="Chat with KRISHI MITRA",
                type="primary",
            ):
                st.session_state.km_chat_open = True
                st.rerun()

        else:

            with st.container(border=True):

                title_col, close_col = st.columns([5, 1])

                with title_col:
                    st.markdown("### 🌱 KRISHI MITRA")

                with close_col:
                    if st.button("✕", key="km_close_chat"):
                        st.session_state.km_chat_open = False
                        st.rerun()

                st.caption(
                    "ಕನ್ನಡ ಅಥವಾ English ನಲ್ಲಿ ಕೇಳಿ. "
                    "ಮಾತನಾಡಲು ಮೈಕ್ರೊಫೋನ್ ಒತ್ತಿರಿ."
                )

                if st.button(
                    "🗑️ Clear conversation",
                    key="km_clear_chat",
                ):
                    clear_chat()

                with st.container(height=300):

                    if not st.session_state.km_chat_history:
                        st.markdown(
                            "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ KRISHI MITRA. "
                            "ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಲಿ?"
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
                    "ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಬರೆಯಿರಿ ಅಥವಾ ಮಾತನಾಡಿ...",
                    accept_audio=True,
                    audio_sample_rate=16000,
                    key="km_floating_chat_input",
                )

                if prompt is not None:
                    user_message = (prompt.text or "").strip()

                    if prompt.audio is not None:
                        with st.spinner("ನಿಮ್ಮ ಧ್ವನಿಯನ್ನು ಗುರುತಿಸಲಾಗುತ್ತಿದೆ..."):
                            transcript = transcribe_audio(prompt.audio)

                        if transcript:
                            user_message = transcript
                            st.info(f"ನೀವು ಹೇಳಿದ್ದು: {transcript}")

                    if user_message:
                        with st.spinner("KRISHI MITRA ಉತ್ತರಿಸುತ್ತಿದೆ..."):
                            send_message(user_message)

                        st.rerun()
