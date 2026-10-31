
import streamlit as st

from frontend.i18n import t


def navigate_to(page):
    """Update sidebar selection when a dashboard card is clicked."""
    st.session_state["km_navigation"] = page


def render_service_cards():

    st.markdown(f"## {t('services')}")

    services = [
        {
            "icon": "🏛️",
            "title": t("government_schemes"),
            "description": t("schemes_card_description"),
            "page": "Government Schemes",
        },
        {
            "icon": "🌾",
            "title": t("mandi_prices"),
            "description": t("mandi_card_description"),
            "page": "Mandi Prices",
        },
        {
            "icon": "🍃",
            "title": t("crop_disease_detection"),
            "description": t("disease_card_description"),
            "page": "Crop Disease Detection",
        },
        {
            "icon": "👨‍🌾",
            "title": t("profile"),
            "description": t("profile_card_description"),
            "page": "Profile",
        },
    ]

    for row_start in range(0, len(services), 2):

        columns = st.columns(2)

        for col, service in zip(
            columns,
            services[row_start:row_start + 2],
        ):

            with col:

                with st.container(border=True):

                    st.markdown(f"## {service['icon']}")

                    st.markdown(f"### {service['title']}")

                    st.write(service["description"])

                    st.button(
                        t("next"),
                        key=f"service_{service['page']}",
                        use_container_width=True,
                        on_click=navigate_to,
                        args=(service["page"],),
                    )
