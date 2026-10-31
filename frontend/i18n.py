
import json
from pathlib import Path

import streamlit as st


LOCALES_DIR = Path(__file__).parent / "locales"


SUPPORTED_LANGUAGES = {
    "kn": "ಕನ್ನಡ",
    "en": "English",
}

DEFAULT_LANGUAGE = "kn"


# --------------------------------------------------
# LOAD TRANSLATION FILE
# --------------------------------------------------

@st.cache_data
def load_language_file(language_code: str) -> dict:

    if language_code not in SUPPORTED_LANGUAGES:
        language_code = DEFAULT_LANGUAGE

    file_path = LOCALES_DIR / f"{language_code}.json"

    try:

        with file_path.open("r", encoding="utf-8") as file:
            translations = json.load(file)

        if not isinstance(translations, dict):
            raise ValueError("Translation file must contain a JSON object.")

        return translations

    except FileNotFoundError:

        if language_code != DEFAULT_LANGUAGE:
            return load_language_file(DEFAULT_LANGUAGE)

        raise

    except json.JSONDecodeError as error:

        raise ValueError(
            f"Invalid JSON file: {file_path}"
        ) from error


# --------------------------------------------------
# INITIALIZE LANGUAGE
# --------------------------------------------------

def initialize_language():

    if "language" not in st.session_state:
        st.session_state.language = DEFAULT_LANGUAGE

    if st.session_state.language not in SUPPORTED_LANGUAGES:
        st.session_state.language = DEFAULT_LANGUAGE


# --------------------------------------------------
# GET CURRENT LANGUAGE
# --------------------------------------------------

def get_current_language():

    initialize_language()

    return st.session_state.language


# --------------------------------------------------
# SET LANGUAGE
# --------------------------------------------------

def set_language(language_code):

    if language_code not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"Unsupported language: {language_code}"
        )

    st.session_state.language = language_code


# --------------------------------------------------
# LANGUAGE DISPLAY NAME
# --------------------------------------------------

def get_language_name(language_code):

    return SUPPORTED_LANGUAGES.get(
        language_code,
        SUPPORTED_LANGUAGES[DEFAULT_LANGUAGE],
    )


# --------------------------------------------------
# TRANSLATION FUNCTION
# --------------------------------------------------

def t(key, **kwargs):

    language = get_current_language()

    selected_translations = load_language_file(language)
    english_translations = load_language_file("en")

    value = selected_translations.get(key)

    # English fallback if a Kannada translation is missing
    if value is None:
        value = english_translations.get(key)

    # Key fallback if translation is missing in both files
    if value is None:
        value = key

    if kwargs:

        try:
            value = value.format(**kwargs)

        except (KeyError, ValueError):
            pass

    return value
