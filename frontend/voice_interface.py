
import requests
import streamlit as st


CHAT_API_URL = "http://127.0.0.1:8000/api/chat/message"


def initialize_chat():
    if "km_chat_history" not in st.session_state:
        st.session_state.km_chat_history = []


def clear_chat():
    st.session_state.km_chat_history = []
    st.rerun()


def send_message(message: str):
    history = st.session_state.km_chat_history

    # Keep the most recent 12 messages for context.
    recent_history = history[-12:]

    try:
        response = requests.post(
            CHAT_API_URL,
            json={
                "message": message,
                "history": recent_history,
            },
            timeout=60,
        )

        response.raise_for_status()
        data = response.json()

        if not data.get("success") or not data.get("reply"):
            st.error("The assistant could not generate a response.")
            return

        history.append({
            "role": "user",
            "content": message,
        })

        history.append({
            "role": "assistant",
            "content": data["reply"],
        })

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to KRISHI MITRA backend. "
            "Please check whether FastAPI is running."
        )

    except requests.exceptions.Timeout:
        st.error("The assistant took too long to respond. Please try again.")

    except requests.exceptions.HTTPError as error:
        try:
            detail = response.json().get("detail", str(error))
        except Exception:
            detail = str(error)

        st.error(f"Chat API error: {detail}")

    except Exception as error:
        st.error(f"Something went wrong: {error}")


def render_voice_interface():
    initialize_chat()

    st.markdown("## 🌱 KRISHI MITRA Assistant")
    st.caption(
        "ನಿಮ್ಮ ಪ್ರಶ್ನೆಗಳನ್ನು ಕನ್ನಡ ಅಥವಾ English ನಲ್ಲಿ ಕೇಳಬಹುದು."
    )

    top_left, top_right = st.columns([5, 1])

    with top_right:
        if st.button(
            "🗑️ Clear",
            use_container_width=True,
            key="km_clear_chat",
        ):
            clear_chat()

    # Display conversation.
    for message in st.session_state.km_chat_history:
        with st.chat_message(
            message["role"],
            avatar="🌱" if message["role"] == "assistant" else "👨‍🌾",
        ):
            st.markdown(message["content"])

    # Chat input.
    user_message = st.chat_input(
        "ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಇಲ್ಲಿ ಬರೆಯಿರಿ..."
    )

    if user_message and user_message.strip():
        with st.chat_message("user", avatar="👨‍🌾"):
            st.markdown(user_message)

        with st.chat_message("assistant", avatar="🌱"):
            with st.spinner("KRISHI MITRA ಉತ್ತರಿಸುತ್ತಿದೆ..."):
                send_message(user_message.strip())

        st.rerun()
