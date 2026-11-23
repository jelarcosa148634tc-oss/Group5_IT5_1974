import streamlit as st


def load_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }

        .stApp {
            background-color: #F5F7F6;
        }

        [data-testid="stSidebar"] {
            background-color: #172B25;
        }

        [data-testid="stSidebar"] * {
            color: #F4F7F5;
        }

        h1, h2, h3 {
            font-family: 'Manrope', sans-serif;
            letter-spacing: -0.02em;
        }

        .hero {
            background: linear-gradient(
                120deg,
                #176B4A,
                #103C30
            );
            padding: 32px;
            border-radius: 18px;
            color: white;
        }

        .hero h1 {
            color: white;
            font-size: 2.2rem;
        }

        .hero p {
            color: #D7EEE3;
        }

        div[data-testid="stMetric"] {
            background: white;
            border: 1px solid #E4EAE6;
            padding: 16px;
            border-radius: 14px;
        }

        div.stButton > button {
            border-radius: 9px;
            font-weight: 600;
        }

        </style>
    """, unsafe_allow_html=True)