import streamlit as st
from components.welcome import render_welcome

import streamlit.components.v1 as components

components.html(
    """
    <script>
    window.addEventListener("message", (event) => {
        if (event.data.type === "BROWSER_LOCATION") {
            window.parent.document.dispatchEvent(
                new CustomEvent("locationReady", { detail: event.data.payload })
            );
        }
    });
    </script>
    """,
    height=0,
)

# PAGE CONFIG — CENTERED
st.set_page_config(
    page_title="Road Accident Risk Predictor",
    page_icon="🚦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Render welcome screen
render_welcome()

# Navigation button
if "selected_mode" in st.session_state:
    st.switch_page("pages/dashboard.py")
