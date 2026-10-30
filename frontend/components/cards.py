
import streamlit as st

from frontend.i18n import t


SERVICES = [
    {
        "key": "schemes",
        "icon": "🏛️",
        "title": "schemes",
        "description": "scheme_description",
    },
    {
        "key": "mandi",
        "icon": "🌾",
        "title": "mandi",
        "description": "mandi_description",
    },
    {
        "key": "disease",
        "icon": "🍃",
        "title": "disease",
        "description": "disease_description",
    },
    {
        "key": "profile",
        "icon": "👨‍🌾",
        "title": "profile",
        "description": "profile_description",
    },
]


def _navigate_to(page):
    st.session_state["sidebar_page"] = page


def render_service_cards():
    st.markdown(
        f'<div class="km-section-label">{t("services")}</div>',
        unsafe_allow_html=True,
    )

    columns = st.columns(2)

    for index, service in enumerate(SERVICES):
        with columns[index % 2]:
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div class="km-card-icon">{service["icon"]}</div>
                    <div class="km-card-title">
                        {t(service["title"])}
                    </div>
                    <div class="km-card-description">
                        {t(service["description"])}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.button(
                    t("next"),
                    key=f"service_{service['key']}",
                    use_container_width=True,
                    on_click=_navigate_to,
                    args=(service["key"],),
                )
