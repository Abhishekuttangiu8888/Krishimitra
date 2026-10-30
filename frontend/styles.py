
import streamlit as st


def apply_styles():
    st.markdown(
        """
        <style>
        /* =====================================
           KRISHI MITRA - GLOBAL THEME
        ===================================== */

        :root {
            --km-green: #287a45;
            --km-dark-green: #185c32;
            --km-light-green: #eaf5ec;
            --km-bg: #f7faf7;
            --km-text: #26382b;
            --km-muted: #68786c;
            --km-border: #e1eae2;
        }

        /* Main application background */

        .stApp {
            background-color: var(--km-bg);
            color: var(--km-text);
        }

        .block-container {
            padding-top: 1.8rem;
            padding-bottom: 2rem;
            max-width: 1250px;
        }

        /* BRAND AND LOGO */

        .km-brand {
            display: block;
            width: 100%;
            max-width: 100%;
            color: var(--km-dark-green);
            font-size: clamp(21px, 2.2vw, 28px);
            font-weight: 800;
            line-height: 1.4;
            letter-spacing: 0.2px;
            white-space: normal;
            overflow: visible;
            overflow-wrap: anywhere;
            word-break: normal;
            margin-bottom: 4px;
        }

        .km-tagline {
            display: block;
            width: 100%;
            color: var(--km-muted);
            font-size: 13px;
            line-height: 1.6;
            white-space: normal;
            overflow: visible;
            overflow-wrap: break-word;
        }

        /* SIDEBAR */

        section[data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid var(--km-border);
            min-width: 265px;
            max-width: 285px;
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 1.5rem;
        }

        section[data-testid="stSidebar"] .km-brand {
            font-size: 23px;
            line-height: 1.45;
        }

        section[data-testid="stSidebar"] .km-tagline {
            font-size: 12px;
        }

        section[data-testid="stSidebar"] hr {
            border-color: var(--km-border);
            margin-top: 15px;
            margin-bottom: 15px;
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4 {
            color: var(--km-dark-green);
            font-weight: 750;
        }

        /* Sidebar navigation */

        section[data-testid="stSidebar"] div[role="radiogroup"] {
            gap: 7px;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label {
            padding: 9px 12px;
            border-radius: 9px;
            transition: background-color 0.2s ease;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
            background-color: var(--km-light-green);
        }

        /* WELCOME SECTION */

        .km-welcome {
            background: linear-gradient(
                120deg,
                #e7f5e9,
                #f4faf3
            );
            border: 1px solid #dceede;
            border-radius: 16px;
            padding: 25px 28px;
            margin: 10px 0 25px 0;
        }

        .km-welcome h2 {
            color: var(--km-dark-green);
            font-size: clamp(22px, 3vw, 30px);
            font-weight: 800;
            line-height: 1.4;
            margin-top: 0;
            margin-bottom: 8px;
            overflow-wrap: break-word;
        }

        .km-welcome p {
            color: #536b59;
            font-size: 15px;
            line-height: 1.7;
            margin-bottom: 0;
        }

        /* SECTION LABELS */

        .km-section-label {
            color: var(--km-dark-green);
            font-size: 19px;
            font-weight: 750;
            margin: 22px 0 14px 0;
        }

        /* SERVICE CARDS */

        .km-card-icon {
            font-size: 32px;
            margin-bottom: 10px;
        }

        .km-card-title {
            color: var(--km-dark-green);
            font-size: 18px;
            font-weight: 750;
            margin-bottom: 7px;
        }

        .km-card-description {
            color: var(--km-muted);
            font-size: 13px;
            line-height: 1.6;
            min-height: 42px;
        }

        /* Streamlit bordered containers */

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #ffffff;
            border: 1px solid var(--km-border);
            border-radius: 14px;
            padding: 12px;
        }

        /* BUTTONS */

        .stButton > button {
            border-radius: 9px;
            font-weight: 650;
            min-height: 42px;
            transition: all 0.2s ease;
        }

        .stButton > button[kind="primary"] {
            background-color: var(--km-green);
            border: 1px solid var(--km-green);
            color: #ffffff;
        }

        .stButton > button[kind="primary"]:hover {
            background-color: var(--km-dark-green);
            border-color: var(--km-dark-green);
        }

        .stButton > button[kind="secondary"] {
            border: 1px solid #cbdccb;
            color: var(--km-dark-green);
            background-color: #ffffff;
        }

        .stButton > button[kind="secondary"]:hover {
            border-color: var(--km-green);
            color: var(--km-green);
            background-color: var(--km-light-green);
        }

        /* INPUTS AND SELECTBOXES */

        .stTextInput input,
        .stTextArea textarea,
        .stSelectbox div[data-baseweb="select"] {
            border-radius: 9px;
        }

        /* FOOTER */

        .km-footer {
            text-align: center;
            color: var(--km-muted);
            font-size: 12px;
            line-height: 1.6;
            padding: 25px 10px 10px 10px;
            margin-top: 25px;
            border-top: 1px solid var(--km-border);
        }

        /* RESPONSIVE DESIGN */

        @media (max-width: 768px) {
            .block-container {
                padding: 1rem 1rem 2rem 1rem;
            }

            .km-brand {
                font-size: 22px;
            }

            .km-tagline {
                font-size: 12px;
            }

            .km-welcome {
                padding: 20px;
            }

            .km-welcome h2 {
                font-size: 23px;
            }

            .km-section-label {
                font-size: 17px;
            }
        }

        @media (max-width: 480px) {
            .km-welcome {
                padding: 16px;
            }

            .km-card-title {
                font-size: 16px;
            }

            .km-card-description {
                font-size: 12px;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
