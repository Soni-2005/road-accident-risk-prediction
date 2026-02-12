# ==================================================
# Road Accident Risk Prediction — Dashboard
# FINAL ARCHITECTURE VERSION
#
# ✔ Scoped CSS Layout System
# ✔ .dashboard-root Boundary
# ✔ Welcome Gate Enforcement
# ✔ Single Global Router
# ✔ Mode Switch State Reset
# ✔ Forecast-Aware Time Logic
# ✔ Prediction Context Persistence
# ✔ Debug Hook
# ✔ Dead-Code Strategy
# ✔ Architectural Documentation
# ==================================================

import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from datetime import datetime, date, time, timedelta


# --------------------------------------------------
# PAGE CONFIG — WIDE (MAP NEEDS THIS)
# --------------------------------------------------
st.set_page_config(
    page_title="Road Accident Risk Prediction — Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------
# 🚨 HARD GUARD — PREVENT DIRECT ACCESS
# --------------------------------------------------
if "selected_mode" not in st.session_state:
    st.switch_page("main.py")

# --------------------------------------------------
# Imports
# --------------------------------------------------
from config import APP_NAME
from services.local_predictor import predict_risk_local as predict_risk
from services.local_predictor import predict_risk_local
from services.weather import get_weather, get_forecast_weather

from components.header import render_header
from components.safety_ribbon import render_safety_ribbon
from components.risk_cards import render_risk_cards
from components.heatmap_legend import render_heatmap_legend
from components.risk_factor_badges import render_risk_factor_badges
from components.weather_card import render_weather_card
from components.risk_interpretation import render_risk_interpretation
from components.risk_badge import render_risk_badge
from components.driver_advice import render_driver_advice




st.markdown("""
<style>
/* Glass container for dashboard content */
.dashboard-glass {
    background: rgba(255, 255, 255, 0.10);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 18px;
    padding: 1.5rem;
    border: 1px solid rgba(255,255,255,0.25);
}

/* Improve readability */
.dashboard-glass h1,
.dashboard-glass h2,
.dashboard-glass h3 {
    color: #ffffff;
}

/* Prevent map blur */
.dashboard-glass iframe {
    backdrop-filter: none !important;
}
</style>
""", unsafe_allow_html=True)



# --------------------------------------------------
# GLOBAL DASHBOARD LAYOUT (SCOPED CSS)
# --------------------------------------------------
def apply_layout_structure():
    """
    SCOPED layout system.
    CSS selectors create boundaries, not files.
    Affects ONLY elements inside .dashboard-root
    """
    st.markdown(
        """
        <style>
        /* ==============================
           DASHBOARD SCOPED LAYOUT SYSTEM
           ============================== */

        .dashboard-root .block-container {
            max-width: 1200px !important;
            margin: 0 auto !important;
            padding: 1rem 1.5rem !important;
        }

        .dashboard-root .main {
            padding: 0 !important;
        }

        .dashboard-root div[data-testid="column"] {
            padding: 0.5rem !important;
        }

        .dashboard-root div[data-testid="stVerticalBlock"] > div {
            gap: 0.6rem !important;
        }

        .dashboard-root iframe {
            border: none;
        }

        .dashboard-root header[data-testid="stHeader"] {
            background: transparent;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# UI POLISH CSS — Risk Results Styling
# --------------------------------------------------
st.markdown("""
<style>
.risk-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    margin-bottom: 16px;
}

.risk-banner {
    border-left: 6px solid #22c55e;
    background: #f0fdf4;
}

.risk-title {
    font-size: 28px;
    font-weight: 700;
    color: #16a34a;
    margin-bottom: 6px;
}

.risk-desc {
    font-size: 16px;
    color: #374151;
}

.metric-title {
    font-size: 14px;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.metric-value {
    font-size: 34px;
    font-weight: 700;
    color: #111827;
}

.severity {
    font-size: 22px;
    font-weight: 600;
    color: #92400e;
}

.factor-pill {
    display: inline-block;
    background: #f3f4f6;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 14px;
    margin: 6px 6px 0 0;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# DEFAULT MODE — LIVE LOCATION
# --------------------------------------------------
def run_default_mode():
    """
    Default Mode:
      - Browser-based live location
      - Current timestamp
      - Live weather
      - Auto-run prediction
    """

    st.markdown("## 🟢 Default Mode — Live Risk Near You")
    st.info("📍 Click the button below to share your location")

    # 1️⃣ Browser geolocation (RELIABLE COMPONENT)
    location = streamlit_geolocation()

    if not location or location["latitude"] is None:
        st.warning("📍 Waiting for location permission...")
        return

    lat = location["latitude"]
    lon = location["longitude"]

    st.success(f"📍 Location captured: {lat:.4f}, {lon:.4f}")

    # 2️⃣ Time + Weather
    hour = datetime.now().hour
    weather = get_weather(lat, lon)

    render_weather_card(weather)

    # 3️⃣ Prediction payload
    payload = {
        "latitude": lat,
        "longitude": lon,
        "hour": hour,
        "weather_condition": weather.get("condition"),
    }

    # Debug hook (safe, optional)
    if st.session_state.get("debug_mode", False):
        st.json(payload)

    try:
        raw_response = predict_risk(payload)

        # ✅ NORMALIZE BACKEND RESPONSE
        risk_response = {
            "risk_level": raw_response.get("risk_level", "Low"),
            "risk_score": raw_response.get("probability_score", 0.0),
            "probability": raw_response.get("probability_score", 0.0) * 100,
            "severity": raw_response.get("severity_context", "Moderate"),
        }

        st.session_state.last_prediction = {
            "weather_condition": weather.get("condition"),
            "hour": hour,
        }

        render_risk_cards(risk_response)
        render_risk_interpretation(risk_response)
        render_driver_advice(
            weather_condition=weather.get("condition"),
            hour=hour
        )
        


    except Exception as e:
        st.error("❌ Live risk prediction failed")
        st.exception(e)


# --------------------------------------------------
# MANUAL MODE — FUTURE SCENARIO ANALYSIS
# --------------------------------------------------
def run_manual_mode():
    """
    Manual Mode:
      - Map click for location
      - Date + 4-hour window
      - Forecast-aware weather (safe fallback)
      - Controlled prediction trigger
      - ZERO runtime errors
    """
    import folium
    from streamlit_folium import st_folium
    from datetime import datetime, date, time, timedelta

    st.markdown("## 🟡 Manual Mode — Scenario Risk Analysis")
    st.info("📍 Click on the map to select a location")

    # -----------------------------
    # Session State Init
    # -----------------------------
    if "manual_location" not in st.session_state:
        st.session_state.manual_location = None

    # -----------------------------
    # MAP SECTION
    # -----------------------------
    default_lat, default_lon = 13.3601, 79.0258
    map_center = st.session_state.manual_location or (default_lat, default_lon)

    map_col, info_col = st.columns([3.5, 1], gap="large")

    with map_col:
        m = folium.Map(location=map_center, zoom_start=13, control_scale=True)

        if st.session_state.manual_location:
            folium.Marker(
                location=st.session_state.manual_location,
                tooltip="Selected Location",
                icon=folium.Icon(color="red"),
            ).add_to(m)

        map_output = st_folium(
            m,
            height=600,
            width="100%",
            returned_objects=["last_clicked"],
            key="manual_map",
        )

        if map_output and map_output.get("last_clicked"):
            st.session_state.manual_location = (
                map_output["last_clicked"]["lat"],
                map_output["last_clicked"]["lng"],
            )

    # -----------------------------
    # SIDE PANEL (Legend + Factors)
    # -----------------------------
    with info_col:
        render_heatmap_legend()

        if st.session_state.get("last_prediction"):
            render_risk_factor_badges(
                weather_condition=st.session_state.last_prediction.get("weather_condition"),
                hour=st.session_state.last_prediction.get("hour"),
            )

    # -----------------------------
    # Location Guard
    # -----------------------------
    if not st.session_state.manual_location:
        st.warning("⚠️ Please click on the map to select a location.")
        return

    st.markdown("---")

    # -----------------------------
    # DATE + TIME WINDOW
    # -----------------------------
    selected_date = st.date_input(
        "Date",
        value=date.today(),
        min_value=date.today(),
    )

    TIME_WINDOWS = {
        "00:00 – 04:00": 0,
        "04:00 – 08:00": 4,
        "08:00 – 12:00": 8,
        "12:00 – 16:00": 12,
        "16:00 – 20:00": 16,
        "20:00 – 24:00": 20,
    }

    window_label = st.selectbox("4-hour window", list(TIME_WINDOWS.keys()))
    start_hour = TIME_WINDOWS[window_label]

    start_timestamp = datetime.combine(selected_date, time(hour=start_hour))
    end_timestamp = start_timestamp + timedelta(hours=4)
    forecast_limit = datetime.utcnow() + timedelta(days=5)

    lat, lon = st.session_state.manual_location

    # -----------------------------
    # WEATHER (SAFE FETCH)
    # -----------------------------
    weather = None

    try:
        if start_timestamp <= forecast_limit:
            weather = get_forecast_weather(
                latitude=lat,
                longitude=lon,
                start_timestamp=start_timestamp.isoformat(),
                end_timestamp=end_timestamp.isoformat(),
            )

        # Fallback if forecast missing or unavailable
        if not weather:
            weather = get_weather(lat, lon)

    except Exception as e:
        st.error("⚠️ Weather service unavailable.")
        st.exception(e)
        return

    # Final safety guard
    if not isinstance(weather, dict):
        st.error("⚠️ Invalid weather data received.")
        return

    # -----------------------------
    # WEATHER UI
    # -----------------------------
    render_weather_card(weather)

    st.markdown("---")

    # -----------------------------
    # RUN PREDICTION
    # -----------------------------
    if st.button("🚦 Run Risk Analysis", key="manual_run"):
        payload = {
            "latitude": float(lat),
            "longitude": float(lon),
            "hour": int(start_hour),
            "weather_condition": weather.get("condition", "Unknown"),
        }

        try:
            raw_response = predict_risk(payload)

            # ✅ NORMALIZE BACKEND RESPONSE
            risk_response = {
                "risk_level": raw_response.get("risk_level", "Low"),
                "risk_score": raw_response.get("probability_score", 0.0),
                "probability": raw_response.get("probability_score", 0.0) * 100,
                "severity": raw_response.get("severity_context", "Moderate"),
            }

            st.session_state.last_prediction = {
                "weather_condition": weather.get("condition"),
                "hour": start_hour,
            }

            st.success("✅ Risk prediction successful")

            render_risk_cards(risk_response)
            render_risk_interpretation(risk_response)
            render_driver_advice(
                weather_condition=weather.get("condition"),
                hour=start_hour
            )



        except Exception as e:
            st.error("❌ Risk prediction failed.")
            st.exception(e)



# ==================================================
# SINGLE GLOBAL ROUTER (DO NOT DUPLICATE)
# ==================================================

apply_layout_structure()

st.markdown('<div class="dashboard-root">', unsafe_allow_html=True)

render_header(APP_NAME)
render_safety_ribbon()

# 🔮 Glassmorphic content starts here
st.markdown('<div class="dashboard-glass">', unsafe_allow_html=True)

MODE = st.session_state.selected_mode


# MODE SWITCH SAFETY RESET
if MODE != st.session_state.get("last_mode"):
    st.session_state.manual_location = None
    st.session_state.last_prediction = None

st.session_state.last_mode = MODE

if MODE == "Default Mode":
    run_default_mode()
else:
    run_manual_mode()

# 🔮 Close glass container
st.markdown('</div>', unsafe_allow_html=True)

# Close dashboard root
st.markdown('</div>', unsafe_allow_html=True)

