import streamlit as st

def render_risk_badge(risk_level: str):
    if not risk_level:
        return

    color_map = {
        "Low": "#22c55e",
        "Moderate": "#facc15",
        "High": "#ef4444",
    }

    color = color_map.get(risk_level, "#94a3b8")

    st.markdown(
        f"""
        <div style="
            display: inline-block;
            padding: 6px 14px;
            border-radius: 999px;
            background: {color};
            color: black;
            font-weight: 700;
            font-size: 14px;
            margin-top: 8px;
        ">
            {risk_level.upper()} RISK
        </div>
        """,
        unsafe_allow_html=True,
    )
