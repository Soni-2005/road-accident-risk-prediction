import streamlit as st

def render_risk_interpretation(risk_response: dict):
    """
    Explains prediction outcome in plain English.
    Reviewer-friendly.
    """

    if not risk_response:
        return

    risk_level = risk_response.get("risk_level", "Unknown")
    probability = risk_response.get("probability")

    st.markdown("### 🧠 Risk Interpretation")

    if risk_level == "Low":
        st.success(
            "🟢 **Low Risk**\n\n"
            "Current conditions suggest a lower likelihood of road accidents. "
            "Maintain safe driving practices and stay alert."
        )

    elif risk_level == "Moderate":
        st.warning(
            "🟡 **Moderate Risk**\n\n"
            "Certain environmental or temporal factors increase accident risk. "
            "Extra caution is advised, especially near intersections or during turns."
        )

    elif risk_level == "High":
        st.error(
            "🔴 **High Risk**\n\n"
            "Conditions indicate a significantly increased accident risk. "
            "Reduce speed, increase following distance, and avoid risky maneuvers."
        )

    if probability is not None:
        st.caption(f"Estimated accident probability: **{probability:.2f}%**")
