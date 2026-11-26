
import streamlit as st


def load_styles():

    st.markdown("""
        <style>

        @import url(
            'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap'
        );

        /* GENERAL */

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }

        .stApp {
            background-color: #F3F5F8;
        }

        h1, h2, h3 {
            font-family: 'Manrope', sans-serif;
            color: #10132F;
            letter-spacing: -0.02em;
        }

        /* HIDE AUTOMATIC STREAMLIT NAVIGATION */

        [data-testid="stSidebarNav"] {
            display: none;
        }

        /* SIDEBAR */

        [data-testid="stSidebar"] {
            background-color: #ECEFF4;
            border-right: 1px solid #E0E5ED;
        }

        [data-testid="stSidebar"] * {
            color: #252B40;
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #10132F;
        }

        /* SIDEBAR NAVIGATION */

        [data-testid="stSidebar"] 
        div[role="radiogroup"] {
            gap: 7px;
        }

        [data-testid="stSidebar"] 
        div[role="radiogroup"] label {
            background-color: transparent;
            padding: 10px 13px;
            border-radius: 10px;
            transition: 0.2s ease;
        }

        [data-testid="stSidebar"] 
        div[role="radiogroup"] label:hover {
            background-color: #DDE8F5;
        }

        [data-testid="stSidebar"] 
        div[role="radiogroup"] label:has(input:checked) {
            background-color: #FFFFFF;
            box-shadow: 0 2px 8px rgba(16, 19, 47, 0.08);
            color: #168BD2;
            font-weight: 700;
        }

        /* HERO SECTION */

        .hero {
            background: linear-gradient(
                120deg,
                #10132F,
                #164B82
            );
            padding: 36px;
            border-radius: 20px;
            color: white;
        }

        .hero h1 {
            color: white;
            font-size: 2.2rem;
        }

        .hero p {
            color: #D8EAFB;
        }

        /* METRIC CARDS */

        div[data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid #E5EAF1;
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 3px 12px rgba(16, 19, 47, 0.04);
        }

        div[data-testid="stMetricLabel"] {
            color: #778196;
        }

        div[data-testid="stMetricValue"] {
            color: #10132F;
        }

        /* CONTENT CARDS */

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #FFFFFF;
            border-radius: 16px;
            border-color: #E5EAF1;
        }

        /* BUTTONS */

        div.stButton > button {
            background-color: #168BD2;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 18px;
            font-weight: 600;
            transition: 0.2s ease;
        }

        div.stButton > button:hover {
            background-color: #106EAB;
            color: white;
            border: none;
        }

        /* INPUTS */

        input, textarea {
            border-radius: 9px !important;
        }

        /* DIVIDERS */

        hr {
            border-color: #E0E5ED;
        }

        </style>
    """, unsafe_allow_html=True)
