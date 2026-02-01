# ==================================================
# UI COMPONENT — RISK CARDS
# Phase 14.2.3c
# ==================================================

import streamlit as st


# --------------------------------------------------
# Risk color mapping
# --------------------------------------------------
RISK_COLORS = {
    "Low": "#4CAF50",
    "Moderate": "#FFC107",
    "High": "#FF9800",
    "Severe": "#F44336",
    "Critical": "#B71C1C",
}


def render_risk_cards(
    probability: float,
    severity: float,
    risk_level: str,
):
    """
    Renders accident probability, severity and final risk level cards.

    Parameters
    ----------
    probability : float
        Probability of accident (0–1)
    severity : float
        Severity score (0–1)
    risk_level : str
        Final risk category
    """

    risk_color = RISK_COLORS.get(risk_level, "#9E9E9E")

    # --------------------------------------------------
    # CSS styling
    # --------------------------------------------------
    st.markdown(
        f"""
        <style>
        .risk-card {{
            background: rgba(0, 0, 0, 0.55);
            border-radius: 18px;
            padding: 22px;
            margin: 10px;
            text-align: center;
            box-shadow: 0px 8px 30px rgba(0,0,0,0.35);
            backdrop-filter: blur(10px);
            color: #ffffff;
        }}

        .risk-value {{
            font-size: 34px;
            font-weight: 700;
            margin-top: 8px;
        }}

        .risk-label {{
            font-size: 15px;
            letter-spacing: 1px;
            text-transform: uppercase;
            opacity: 0.85;
        }}

        .risk-final {{
            border: 2px solid {risk_color};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    # --------------------------------------------------
    # Probability Card
    # --------------------------------------------------
    with col1:
        st.markdown(
            f"""
            <div class="risk-card">
                <div class="risk-label">Accident Probability</div>
                <div class="risk-value">{probability * 100:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------
    # Severity Card
    # --------------------------------------------------
    with col2:
        st.markdown(
            f"""
            <div class="risk-card">
                <div class="risk-label">Accident Severity</div>
                <div class="risk-value">{severity * 100:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------
    # Final Risk Card
    # --------------------------------------------------
    with col3:
        st.markdown(
            f"""
            <div class="risk-card risk-final">
                <div class="risk-label">Overall Risk</div>
                <div class="risk-value" style="color:{risk_color}">
                    {risk_level}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
