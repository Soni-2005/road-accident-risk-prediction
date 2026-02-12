import streamlit.components.v1 as components


def render_risk_factor_badges(weather_condition: str, hour: int):
    # -------- Interpret time --------
    if 0 <= hour < 6:
        time_label = "Night (Low visibility)"
        time_icon = "🌙"
    elif 6 <= hour < 12:
        time_label = "Morning"
        time_icon = "🌅"
    elif 12 <= hour < 18:
        time_label = "Afternoon"
        time_icon = "☀️"
    else:
        time_label = "Evening"
        time_icon = "🌆"

    # -------- Weather icon map --------
    weather_icon_map = {
        "Rain":   "🌧️",
        "Clouds": "☁️",
        "Clear":  "☀️",
        "Fog":    "🌫️",
        "Mist":   "🌫️",
    }
    weather_icon = weather_icon_map.get(weather_condition, "🌦️")

    # ----------------------------------------------------------------
    # FIX: st.components.v1.html() bypasses the Markdown parser entirely.
    # st.markdown() runs content through Python-Markdown first — indented
    # HTML blocks get misread as code blocks (4-space indent = code in
    # CommonMark spec). components.html() sends directly to an iframe,
    # so indentation is irrelevant and HTML renders as intended.
    # ----------------------------------------------------------------
    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
  body {{
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: transparent;
  }}
  .factor-card {{
    background: rgba(0, 0, 0, 0.45);
    padding: 18px 22px;
    border-radius: 16px;
  }}
  .factor-title {{
    color: #ffffff;
    font-size: 16px;
    font-weight: 600;
    margin: 0 0 14px 0;
  }}
  .badge-row {{
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
  }}
  .badge {{
    background: rgba(255, 255, 255, 0.08);
    padding: 10px 14px;
    border-radius: 12px;
    color: #ecf0f1;
    font-size: 14px;
    white-space: nowrap;
  }}
</style>
</head>
<body>
<div class="factor-card">
  <div class="factor-title">⚠️ Influencing Factors at This Location</div>
  <div class="badge-row">
    <div class="badge">{weather_icon} Weather: {weather_condition}</div>
    <div class="badge">{time_icon} Time: {time_label}</div>
    <div class="badge">🚧 Road Context: Urban / Junction-prone</div>
  </div>
</div>
</body>
</html>"""

    components.html(html, height=120, scrolling=True)