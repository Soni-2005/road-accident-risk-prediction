# ==================================================
# Streamlit App — DEFAULT MODE (FINAL, STABLE)
# Phase 14.3
# ==================================================

import streamlit as st
from datetime import datetime
from pathlib import Path

# --------------------------------------------------
# Config
# --------------------------------------------------
from config import APP_NAME

# Services (DO NOT CHANGE SIGNATURES)
from services.location import get_browser_location

from services.api import predict_risk
from services.weather import get_weather

# Components
from components.header import render_header
from components.safety_ribbon import render_safety_ribbon
from components.risk_cards import render_risk_cards
from components.map_view import render_map
from components.weather_panel import render_weather_panel


# --------------------------------------------------
# Page setup
# --------------------------------------------------
st.set_page_config(
    page_title=APP_NAME,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------
# Background styling (LOCAL ASSET)
# --------------------------------------------------
ASSETS_DIR = Path(__file__).parent / "assets"
BG_IMAGE = ASSETS_DIR / "background.jpg"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: url("{BG_IMAGE.as_posix()}") no-repeat center center fixed;
        background-size: cover;
    }}

    /* Remove white Streamlit containers */
    section[data-testid="stSidebar"] {{
        background: transparent !important;
    }}

    div[data-testid="stVerticalBlock"],
    div[data-testid="stHorizontalBlock"],
    div.stContainer,
    .block-container {{
        background: transparent !important;
    }}

    /* Hide Streamlit chrome */
    footer {{ visibility: hidden; }}
    #MainMenu {{ visibility: hidden; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# DEFAULT MODE PIPELINE
# --------------------------------------------------
def run_default_mode():
    """
    Runs default (automatic) mode:
    - waits for location
    - fetches weather
    - calls backend
    - renders UI
    """

    # --------------------------------------------------
    # Location (browser / fallback logic is INSIDE service)
    # --------------------------------------------------
    location = get_browser_location()

    if location is None:
        st.info("📍 Waiting for location permission… Please allow access.")
        st.stop()

    lat, lon, location_name = location

    # --------------------------------------------------
    # Weather (automatic)
    # --------------------------------------------------
    weather = get_weather(lat, lon)

    # --------------------------------------------------
    # Backend inference (STRICT API CONTRACT)
    # --------------------------------------------------
    risk_response = predict_risk(
        latitude=lat,
        longitude=lon,
        timestamp=datetime.utcnow().isoformat(),
        weather=weather,
    )

    # --------------------------------------------------
    # UI Rendering
    # --------------------------------------------------
    render_header(APP_NAME, location_name)
    render_safety_ribbon()

    render_risk_cards(
        probability=risk_response["probability"],
        severity=risk_response["severity"],
        risk_level=risk_response["risk_level"],
    )

    col1, col2 = st.columns([1.2, 1])

    with col1:
        render_map(lat, lon)

    with col2:
        render_weather_panel(weather)


# --------------------------------------------------
# App entry
# --------------------------------------------------
run_default_mode()
