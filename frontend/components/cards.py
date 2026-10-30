
import streamlit as st

from frontend.i18n import t


def navigate_to(page):
    """Update sidebar selection when a dashboard card is clicked."""
    st.session_state["km_navigation"] = page


def render_service_cards():

    st.markdown(
        f"## {t('services')}",
    )

    services = [
        {
            "icon": "🏛️",
            "title": "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು",
            "description": "ನಿಮ್ಮ ಕೃಷಿಗೆ ಸೂಕ್ತವಾದ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಿ",
            "page": "Government Schemes",
        },
        {
            "icon": "🌾",
            "title": "ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು",
            "description": "ನಿಮ್ಮ ಹತ್ತಿರದ ಮಾರುಕಟ್ಟೆಗಳ ಬೆಲೆಗಳನ್ನು ತಿಳಿಯಿರಿ",
            "page": "Mandi Prices",
        },
        {
            "icon": "🍃",
            "title": "ಬೆಳೆ ರೋಗ ಪತ್ತೆ",
            "description": "ಬೆಳೆಗಳ ರೋಗಗಳ ಬಗ್ಗೆ ಮಾಹಿತಿ ಪಡೆಯಿರಿ",
            "page": "Crop Disease Detection",
        },
        {
            "icon": "👨‍🌾",
            "title": "ರೈತರ ವಿವರಗಳು",
            "description": "ನಿಮ್ಮ ಕೃಷಿ ವಿವರಗಳನ್ನು ನಿರ್ವಹಿಸಿ",
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

                    st.markdown(
                        f"## {service['icon']}"
                    )

                    st.markdown(
                        f"### {service['title']}"
                    )

                    st.write(service["description"])

                    st.button(
                        "ಮುಂದೆ",
                        key=f"service_{service['page']}",
                        use_container_width=True,
                        on_click=navigate_to,
                        args=(service["page"],),
                    )
