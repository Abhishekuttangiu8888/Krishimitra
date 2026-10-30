
import streamlit as st
import requests

st.set_page_config(page_title="KRISHI MITRA - Voice Test")

API_URL = "http://127.0.0.1:8000/api"

st.title("🌱 KRISHI MITRA")
st.subheader("Kannada Voice Recognition Test")

st.write("ಮೈಕ್ರೊಫೋನ್ ಒತ್ತಿ ಕನ್ನಡದಲ್ಲಿ ಮಾತನಾಡಿ.")

audio = st.audio_input("ನಿಮ್ಮ ಧ್ವನಿಯನ್ನು ರೆಕಾರ್ಡ್ ಮಾಡಿ")

if audio is not None:

    st.audio(audio)

    if st.button("Convert Speech to Text", type="primary"):

        with st.spinner("ನಿಮ್ಮ ಮಾತುಗಳನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳುತ್ತಿದ್ದೇನೆ..."):

            try:
                response = requests.post(
                    f"{API_URL}/voice/transcribe",
                    files={
                        "audio": (
                            "recording.wav",
                            audio.getvalue(),
                            "audio/wav"
                        )
                    },
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()

                    st.success("ಮಾತುಗಳನ್ನು ಗುರುತಿಸಲಾಗಿದೆ!")

                    st.write("Recognized Kannada text:")

                    st.text_area(
                        "ನಿಮ್ಮ ಮಾತುಗಳು",
                        value=result["text"],
                        height=120
                    )

                else:
                    st.error(response.text)

            except requests.RequestException as error:
                st.error(f"Connection error: {error}")
