
import json
from pathlib import Path

import streamlit as st


LOCALES_DIR = Path(__file__).resolve().parent / "locales"

SUPPORTED_LANGUAGES = {
    "kn": "ಕನ್ನಡ",
    "en": "English",
}

DEFAULT_LANGUAGE = "kn"


@st.cache_data
def load_language_file(language_code: str) -> dict:
    if language_code not in SUPPORTED_LANGUAGES:
        language_code = DEFAULT_LANGUAGE

    file_path = LOCALES_DIR / f"{language_code}.json"

    if not file_path.is_file():
        if language_code != DEFAULT_LANGUAGE:
            return load_language_file(DEFAULT_LANGUAGE)

        raise FileNotFoundError(
            f"Kannada translation file not found: {file_path}"
        )

    try:
        with file_path.open("r", encoding="utf-8-sig") as file:
            translations = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in translation file: {file_path}. "
            f"Line: {error.lineno}, Column: {error.colno}"
        ) from error

    if not isinstance(translations, dict):
        raise ValueError(
            f"Translation file must contain a JSON object: {file_path}"
        )

    return translations


def initialize_language() -> None:
    if "language" not in st.session_state:
        st.session_state.language = DEFAULT_LANGUAGE

    if st.session_state.language not in SUPPORTED_LANGUAGES:
        st.session_state.language = DEFAULT_LANGUAGE


def get_current_language() -> str:
    initialize_language()
    return st.session_state.language


def set_language(language_code: str) -> None:
    if language_code not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {language_code}")

    st.session_state.language = language_code


def get_language_name(language_code: str) -> str:
    return SUPPORTED_LANGUAGES.get(
        language_code,
        SUPPORTED_LANGUAGES[DEFAULT_LANGUAGE],
    )


def t(key: str, **kwargs) -> str:
    language = get_current_language()

    selected_translations = load_language_file(language)
    english_translations = load_language_file("en")

    value = selected_translations.get(key)

    if value is None:
        value = english_translations.get(key)

    if value is None:
        value = key

    if not isinstance(value, str):
        return str(value)

    if kwargs:
        try:
            value = value.format(**kwargs)
        except (KeyError, ValueError, IndexError):
            pass

    return value
