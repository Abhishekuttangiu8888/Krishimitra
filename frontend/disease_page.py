
import hashlib

import requests
import streamlit as st

from frontend.voice_interface import transcribe_audio


API_BASE = "http://127.0.0.1:8000/api"
MAX_IMAGE_SIZE = 5 * 1024 * 1024


TEXT = {
    "en": {
        "title": "🌿 Crop Disease Detection",
        "subtitle": "Upload a crop photo to get an AI-assisted health assessment.",
        "upload": "Upload crop image",
        "camera": "Take a crop photo",
        "crop": "Which crop is affected?",
        "crop_placeholder": "Enter crop name",
        "crop_voice": "🎤 Speak crop name",
        "description_voice": "🎤 Describe the crop problem by voice",
        "voice_crop_success": "Crop name recognized",
        "voice_description_success": "Crop description recognized",
        "part": "Which part is affected?",
        "parts": [
            "Leaves",
            "Stem",
            "Roots",
            "Fruits",
            "Flowers",
            "Whole plant",
            "Not sure",
        ],
        "symptoms": "Describe what you observe",
        "symptoms_placeholder": "Example: Yellow spots on leaves...",
        "duration": "How long have you noticed the problem?",
        "durations": [
            "Today",
            "2–3 days",
            "About a week",
            "More than a week",
            "Not sure",
        ],
        "analyze": "🔍 Analyze crop image",
        "analyzing": "Analyzing your crop image...",
        "result": "AI assessment",
        "warning": "This is a preliminary AI assessment, not a confirmed diagnosis.",
        "missing_crop": "Please enter the crop name.",
        "missing_image": "Please upload or capture a crop image.",
        "large_image": "Image must be 5 MB or smaller.",
        "error": "Something went wrong",
        "profile": "Your saved farmer profile",
        "district": "District",
        "village": "Village",
        "saved_crops": "Saved crops",
        "no_profile": "Farmer profile could not be loaded. You can still enter your crop below.",
        "no_results": "No analysis is available yet.",
        "recognizing": "Recognizing your voice...",
    },

    "kn": {
        "title": "🌿 ಬೆಳೆ ರೋಗ ಪತ್ತೆ",
        "subtitle": "ಬೆಳೆಯ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ AI ಮೂಲಕ ಪ್ರಾಥಮಿಕ ಪರಿಶೀಲನೆ ಪಡೆಯಿರಿ.",
        "upload": "ಬೆಳೆಯ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        "camera": "ಕ್ಯಾಮೆರಾದಲ್ಲಿ ಫೋಟೋ ತೆಗೆಯಿರಿ",
        "crop": "ಯಾವ ಬೆಳೆಗೆ ಸಮಸ್ಯೆಯಾಗಿದೆ?",
        "crop_placeholder": "ಬೆಳೆಯ ಹೆಸರನ್ನು ನಮೂದಿಸಿ",
        "crop_voice": "🎤 ಬೆಳೆಯ ಹೆಸರನ್ನು ಧ್ವನಿಯ ಮೂಲಕ ಹೇಳಿ",
        "description_voice": "🎤 ಬೆಳೆಯ ಸಮಸ್ಯೆಯನ್ನು ಧ್ವನಿಯ ಮೂಲಕ ವಿವರಿಸಿ",
        "voice_crop_success": "ಬೆಳೆಯ ಹೆಸರು ಗುರುತಿಸಲಾಗಿದೆ",
        "voice_description_success": "ಬೆಳೆಯ ವಿವರಣೆ ಗುರುತಿಸಲಾಗಿದೆ",
        "part": "ಯಾವ ಭಾಗಕ್ಕೆ ಸಮಸ್ಯೆಯಾಗಿದೆ?",
        "parts": [
            "ಎಲೆಗಳು",
            "ಕಾಂಡ",
            "ಬೇರುಗಳು",
            "ಹಣ್ಣುಗಳು",
            "ಹೂವುಗಳು",
            "ಇಡೀ ಗಿಡ",
            "ಗೊತ್ತಿಲ್ಲ",
        ],
        "symptoms": "ನೀವು ಗಮನಿಸಿದ ಲಕ್ಷಣಗಳನ್ನು ವಿವರಿಸಿ",
        "symptoms_placeholder": "ಉದಾಹರಣೆ: ಎಲೆಗಳಲ್ಲಿ ಹಳದಿ ಕಲೆಗಳು...",
        "duration": "ಈ ಸಮಸ್ಯೆ ಎಷ್ಟು ದಿನಗಳಿಂದ ಇದೆ?",
        "durations": [
            "ಇಂದು",
            "2–3 ದಿನಗಳು",
            "ಸುಮಾರು ಒಂದು ವಾರ",
            "ಒಂದು ವಾರಕ್ಕಿಂತ ಹೆಚ್ಚು",
            "ಗೊತ್ತಿಲ್ಲ",
        ],
        "analyze": "🔍 ಬೆಳೆ ಫೋಟೋ ಪರಿಶೀಲಿಸಿ",
        "analyzing": "ನಿಮ್ಮ ಬೆಳೆಯ ಫೋಟೋ ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ...",
        "result": "AI ಪರಿಶೀಲನೆಯ ಫಲಿತಾಂಶ",
        "warning": "ಇದು AI ನೀಡಿದ ಪ್ರಾಥಮಿಕ ಅಂದಾಜು ಮಾತ್ರ. ಖಚಿತ ರೋಗನಿರ್ಣಯವಲ್ಲ.",
        "missing_crop": "ದಯವಿಟ್ಟು ಬೆಳೆಯ ಹೆಸರನ್ನು ನಮೂದಿಸಿ.",
        "missing_image": "ದಯವಿಟ್ಟು ಬೆಳೆಯ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಅಥವಾ ತೆಗೆದುಕೊಳ್ಳಿ.",
        "large_image": "ಫೋಟೋದ ಗಾತ್ರ 5 MB ಅಥವಾ ಅದಕ್ಕಿಂತ ಕಡಿಮೆ ಇರಬೇಕು.",
        "error": "ದೋಷ ಸಂಭವಿಸಿದೆ",
        "profile": "ನಿಮ್ಮ ಉಳಿಸಿದ ರೈತರ ಪ್ರೊಫೈಲ್",
        "district": "ಜಿಲ್ಲೆ",
        "village": "ಗ್ರಾಮ",
        "saved_crops": "ಉಳಿಸಿದ ಬೆಳೆಗಳು",
        "no_profile": "ರೈತರ ಪ್ರೊಫೈಲ್ ಲೋಡ್ ಆಗಲಿಲ್ಲ. ಕೆಳಗೆ ಬೆಳೆಯ ಹೆಸರನ್ನು ನಮೂದಿಸಬಹುದು.",
        "no_results": "ಇನ್ನೂ ಯಾವುದೇ ಪರಿಶೀಲನೆ ಲಭ್ಯವಿಲ್ಲ.",
        "recognizing": "ನಿಮ್ಮ ಧ್ವನಿಯನ್ನು ಗುರುತಿಸಲಾಗುತ್ತಿದೆ...",
    },
}


def get_auth_headers():
    token = st.session_state.get("km_token")

    if not token:
        return None

    return {"Authorization": f"Bearer {token}"}


def get_farmer_profile():
    headers = get_auth_headers()

    if not headers:
        return None

    try:
        response = requests.get(
            f"{API_BASE}/farmer/profile",
            headers=headers,
            timeout=15,
        )

        if response.status_code == 200:
            return response.json()

    except requests.RequestException:
        pass

    return None


def get_saved_crops(profile):
    crops = profile.get("crops", []) if profile else []

    if not isinstance(crops, list):
        return []

    return [
        str(crop).strip()
        for crop in crops
        if str(crop).strip()
    ]


def render_profile(profile, language):
    t = TEXT[language]

    if not profile:
        st.info(t["no_profile"])
        return

    with st.expander(t["profile"], expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            st.write(
                f"**{t['district']}:** "
                f"{profile.get('district') or '-'}"
            )

        with col2:
            st.write(
                f"**{t['village']}:** "
                f"{profile.get('village') or '-'}"
            )

        crops = get_saved_crops(profile)

        if crops:
            st.write(
                f"**{t['saved_crops']}:** "
                + ", ".join(crops)
            )


def process_voice_input(audio_file, state_key, processed_key, language):
    if audio_file is None:
        return

    audio_bytes = audio_file.getvalue()

    if not audio_bytes:
        return

    audio_hash = hashlib.sha256(audio_bytes).hexdigest()

    # Prevent the same recording from being transcribed repeatedly.
    if st.session_state.get(processed_key) == audio_hash:
        return

    with st.spinner(TEXT[language]["recognizing"]):
        transcript = transcribe_audio(audio_file)

    if transcript:
        st.session_state[state_key] = transcript
        st.session_state[processed_key] = audio_hash
        st.success(transcript)


def analyze_image(
    image_bytes,
    mime_type,
    crop_name,
    symptoms,
    affected_part,
    duration,
):
    headers = get_auth_headers()

    if not headers:
        return None, "Authentication token not found. Please log in again."

    try:
        response = requests.post(
            f"{API_BASE}/agriculture/disease/analyze",
            headers=headers,
            files={
                "image": (
                    "crop_image",
                    image_bytes,
                    mime_type,
                )
            },
            data={
                "crop_name": crop_name,
                "symptoms": symptoms,
                "affected_part": affected_part,
                "duration": duration,
            },
            timeout=120,
        )

        if response.status_code == 200:
            return response.json().get("data"), None

        try:
            error_message = response.json().get(
                "detail",
                "Unable to analyze the image.",
            )
        except ValueError:
            error_message = "Unable to analyze the image."

        return None, error_message

    except requests.Timeout:
        return None, "The analysis timed out. Please try again."

    except requests.RequestException:
        return None, "Cannot connect to the KRISHI MITRA backend."


def render_disease_result(result, language):
    t = TEXT[language]

    if not result:
        st.info(t["no_results"])
        return

    st.divider()
    st.subheader(t["result"])

    st.warning(t["warning"])

    st.markdown(
        result.get("assessment", "No assessment returned.")
    )

    st.caption(
        "The AI result should be checked with a qualified "
        "agricultural expert before applying chemical treatments."
    )


def render_disease_page():
    profile = get_farmer_profile()

    language = "kn"

    if profile and profile.get("preferred_language") == "en":
        language = "en"

    t = TEXT[language]

    st.title(t["title"])
    st.write(t["subtitle"])

    render_profile(profile, language)

    st.divider()

    # Crop name: voice input and manual typing.
    st.subheader(t["crop"])

    crop_audio = st.audio_input(
        t["crop_voice"],
        sample_rate=16000,
        key="km_disease_crop_audio",
    )

    process_voice_input(
        crop_audio,
        "km_disease_crop",
        "km_disease_crop_audio_processed",
        language,
    )

    crop_name = st.text_input(
        t["crop_placeholder"],
        key="km_disease_crop",
    )

    st.divider()

    # Crop image upload or camera.
    st.subheader(t["upload"])

    uploaded_image = st.file_uploader(
        t["upload"],
        type=["jpg", "jpeg", "png", "webp"],
        key="km_disease_upload",
    )

    camera_image = st.camera_input(
        t["camera"],
        key="km_disease_camera",
    )

    selected_image = camera_image or uploaded_image

    if selected_image:
        st.image(
            selected_image,
            caption="Selected crop image",
            use_container_width=True,
        )

    st.divider()

    # Affected plant part.
    st.subheader(t["part"])

    affected_part = st.selectbox(
        t["part"],
        t["parts"],
        key="km_disease_part",
    )

    # Symptoms: voice input and manual typing.
    st.subheader(t["symptoms"])

    description_audio = st.audio_input(
        t["description_voice"],
        sample_rate=16000,
        key="km_disease_description_audio",
    )

    process_voice_input(
        description_audio,
        "km_disease_symptoms",
        "km_disease_description_audio_processed",
        language,
    )

    symptoms = st.text_area(
        t["symptoms"],
        placeholder=t["symptoms_placeholder"],
        key="km_disease_symptoms",
    )

    # Duration.
    duration = st.selectbox(
        t["duration"],
        t["durations"],
        key="km_disease_duration",
    )

    # Analyze.
    if st.button(
        t["analyze"],
        type="primary",
        use_container_width=True,
    ):

        if not crop_name.strip():
            st.error(t["missing_crop"])

        elif selected_image is None:
            st.error(t["missing_image"])

        else:
            image_bytes = selected_image.getvalue()

            if len(image_bytes) > MAX_IMAGE_SIZE:
                st.error(t["large_image"])

            else:
                mime_type = selected_image.type

                with st.spinner(t["analyzing"]):
                    result, error = analyze_image(
                        image_bytes=image_bytes,
                        mime_type=mime_type,
                        crop_name=crop_name.strip(),
                        symptoms=symptoms.strip(),
                        affected_part=affected_part,
                        duration=duration,
                    )

                if error:
                    st.error(f"{t['error']}: {error}")

                elif result:
                    st.session_state["km_disease_result"] = result

    render_disease_result(
        st.session_state.get("km_disease_result"),
        language,
    )
