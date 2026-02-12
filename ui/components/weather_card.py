import streamlit as st

def render_weather_card(weather: dict):
    """
    Renders weather info safely for both
    current and forecast weather payloads.
    """

    if not weather:
        st.warning("Weather data unavailable")
        return

    col1, col2, col3 = st.columns(3)

    # 🌡️ Temperature (always present)
    col1.metric(
        "🌡️ Temperature",
        f"{weather.get('temperature', '—')} °C"
    )

    # 💧 Humidity (may be missing in forecast)
    humidity = weather.get("humidity")
    col2.metric(
        "💧 Humidity",
        f"{humidity} %" if humidity is not None else "N/A"
    )

    # 🌬️ Wind Speed (optional)
    wind = weather.get("wind_speed")
    col3.metric(
        "🌬️ Wind Speed",
        f"{wind} m/s" if wind is not None else "N/A"
    )

    # 🌦️ Condition + Source
    st.caption(
        f"Condition: **{weather.get('condition', 'Unknown')}** "
        f"• Source: **{weather.get('source', 'unknown')}**"
    )
