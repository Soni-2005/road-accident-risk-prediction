import streamlit as st

def render_weather_panel(result: dict):
    st.subheader("🌦️ Weather Context")
    st.write(result.get("weather_condition", "Not available"))
