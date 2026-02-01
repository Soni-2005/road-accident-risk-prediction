import streamlit as st

def render_metrics(result: dict):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Accident Probability",
            value=f"{result.get('probability_score', 0):.2f}"
        )

    with col2:
        st.metric(
            label="Severity Level",
            value=result.get("severity_level", "Unknown")
        )

    with col3:
        st.metric(
            label="Final Risk",
            value=result.get("risk_level", "Unknown")
        )
