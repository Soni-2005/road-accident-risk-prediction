import streamlit as st

def render_header(location):
    col1, col2 = st.columns([4, 1])

    with col1:
        st.markdown(
            """
            <h2 style='text-align:center;'>🚦 Road Accident Risk Prediction System</h2>
            <p style='text-align:center;'>AI-driven Real-Time Road Safety Intelligence</p>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        if location:
            st.markdown("📍 Location Active")
        else:
            st.markdown("📍 Requesting location...")
