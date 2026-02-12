import streamlit as st

def render_driver_advice(weather_condition: str, hour: int):
    st.markdown("### 🚘 Driver Safety Advice")

    tips = []

    if weather_condition in ["Rain", "Drizzle", "Thunderstorm"]:
        tips.append("🌧️ Reduce speed and increase braking distance on wet roads.")

    if weather_condition in ["Fog", "Mist", "Haze"]:
        tips.append("🌫️ Use low-beam headlights and maintain lane discipline.")

    if hour >= 20 or hour <= 5:
        tips.append("🌙 Night-time driving detected — watch for reduced visibility.")

    tips.append("🛣️ Be cautious near intersections, curves, and uneven road surfaces.")

    for tip in tips:
        st.info(tip)
