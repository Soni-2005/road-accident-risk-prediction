import streamlit as st

def render_risk_cards(risk_response: dict):
    """
    2 + 2 Risk Card Layout
    """

    risk_level = risk_response.get("risk_level", "Low")
    probability = risk_response.get("probability", 0.0)
    severity = risk_response.get("severity", "Moderate")
    risk_score = risk_response.get("risk_score", None)

    # ===============================
    # ROW 1 — Risk Level + Risk Score
    # ===============================
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="risk-card">
                <div class="metric-title">Risk Level</div>
                <div class="risk-title">🚦 {risk_level}</div>
                <div class="risk-desc">
                    Overall accident likelihood
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="risk-card">
                <div class="metric-title">Risk Score (0–1)</div>
                <div class="metric-value">
                    {f"{risk_score:.2f}" if risk_score is not None else "—"}
                </div>
                <div class="risk-desc">
                    Normalized model confidence
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ===============================
    # ROW 2 — Probability + Severity
    # ===============================
    col3, col4 = st.columns(2)

    with col3:
        st.markdown(
            f"""
            <div class="risk-card">
                <div class="metric-title">Accident Probability</div>
                <div class="metric-value">{probability:.2f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="risk-card">
                <div class="metric-title">Severity Context</div>
                <div class="severity">{severity}</div>
                <div style="color:#6b7280;font-size:14px;">
                    (historical baseline)
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
