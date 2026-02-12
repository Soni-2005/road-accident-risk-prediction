import streamlit as st


def render_risk_legend():
    st.markdown(
        """
        <div style="
            background: rgba(0,0,0,0.45);
            padding: 16px;
            border-radius: 14px;
            margin-top: 12px;
        ">
            <h4 style="color:#ecf0f1; margin-bottom:10px;">
                🎨 Risk Level Legend
            </h4>

            <div style="display:flex; align-items:center; margin-bottom:6px;">
                <div style="width:14px; height:14px; background:#2ecc71; border-radius:50%; margin-right:10px;"></div>
                <span style="color:#ecf0f1;">Low Risk — conditions generally safe</span>
            </div>

            <div style="display:flex; align-items:center; margin-bottom:6px;">
                <div style="width:14px; height:14px; background:#f1c40f; border-radius:50%; margin-right:10px;"></div>
                <span style="color:#ecf0f1;">Medium Risk — increased caution required</span>
            </div>

            <div style="display:flex; align-items:center;">
                <div style="width:14px; height:14px; background:#e74c3c; border-radius:50%; margin-right:10px;"></div>
                <span style="color:#ecf0f1;">High Risk — accident-prone conditions</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_factor_explanation(risk_response: dict):
    factors = risk_response.get("explanation", {}).get("key_factors", [])

    readable_map = {
        "Hour": "Time of travel influences visibility and traffic patterns",
        "Weather": "Weather conditions affect road grip and driver awareness",
        "Speed": "Higher speeds reduce reaction time and increase impact severity",
    }

    rendered_factors = []

    for f in factors:
        for key in readable_map:
            if key.lower() in f.lower():
                rendered_factors.append(readable_map[key])

    if not rendered_factors:
        rendered_factors.append(
            "Risk is estimated using spatial, temporal, and environmental factors"
        )

    st.markdown(
        """
        <div style="
            background: rgba(0,0,0,0.45);
            padding: 16px;
            border-radius: 14px;
            margin-top: 12px;
        ">
            <h4 style="color:#ecf0f1; margin-bottom:10px;">
                🧠 Factors Influencing Risk
            </h4>
        """,
        unsafe_allow_html=True,
    )

    for item in rendered_factors:
        st.markdown(
            f"""
            <p style="color:#ecf0f1; margin:4px 0;">
                • {item}
            </p>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
