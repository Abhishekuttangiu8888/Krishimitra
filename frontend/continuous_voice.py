
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


_COMPONENT_DIR = Path(__file__).parent / "continuous_voice_component"

_continuous_voice = components.declare_component(
    "krishi_mitra_continuous_voice",
    path=str(_COMPONENT_DIR),
)


def render_continuous_voice(
    question_id: str,
    listening_enabled: bool = True,
):
    language = st.session_state.get("language", "kn")

    if language not in ("kn", "en"):
        language = "kn"

    return _continuous_voice(
        question_id=question_id,
        listening_enabled=listening_enabled,
        language=language,
        default=None,
        key="km_continuous_voice",
    )
