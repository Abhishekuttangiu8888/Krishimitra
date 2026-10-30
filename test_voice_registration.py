
import streamlit as st

from frontend.voice_registration import render_voice_registration

st.set_page_config(page_title="KRISHI MITRA Voice Registration")

render_voice_registration()
