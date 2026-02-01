# ==================================================
# UI COMPONENT — SAFETY RIBBON
# Phase 14.2.3a
# ==================================================

import streamlit as st
import time


SAFETY_MESSAGES = [
    "🚫 Don’t drink and drive",
    "🪖 Always wear a helmet / seatbelt",
    "⚠️ Slow down near junctions",
    "🌧️ Reduce speed during rain",
    "🚸 Watch out for pedestrians",
    "🔦 Use headlights at night",
    "🛣️ Beware of sharp curves ahead",
]


def render_safety_ribbon():
    """
    Renders an animated safety ribbon with rotating safety messages.
    """

    # Inject CSS for ribbon styling & animation
    st.markdown(
        """
        <style>
        .safety-ribbon {
            width: 100%;
            padding: 12px;
            margin-top: 10px;
            margin-bottom: 20px;
            text-align: center;
            font-size: 18px;
            font-weight: 600;
            color: #ffffff;
            background: linear-gradient(
                270deg,
                rgba(255, 87, 34, 0.9),
                rgba(255, 193, 7, 0.9),
                rgba(76, 175, 80, 0.9)
            );
            background-size: 600% 600%;
            border-radius: 12px;
            animation: gradientMove 8s ease infinite;
        }

        @keyframes gradientMove {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Session state to rotate messages
    if "safety_index" not in st.session_state:
        st.session_state.safety_index = 0

    message = SAFETY_MESSAGES[st.session_state.safety_index]

    st.markdown(
        f"""
        <div class="safety-ribbon">
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Rotate message every render cycle
    st.session_state.safety_index = (
        st.session_state.safety_index + 1
    ) % len(SAFETY_MESSAGES)
