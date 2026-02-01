# ==================================================
# PHASE 13.5 — BACKEND WEATHER API INTEGRATION
# ==================================================
# Adds real-time weather context to backend inference
# Weather is fetched in backend and mapped to ML feature
# ==================================================

# --------------------------------------------------
# 1. backend/app/services/weather.py
# --------------------------------------------------
import requests
from backend.app.config import WEATHER_API_KEY

# Example shown for OpenWeatherMap
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather(lat: float, lon: float) -> str:
    """
    Fetch current weather and map it to ML Weather_Conditions
    Returns a string compatible with training categories
    """
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": WEATHER_API_KEY,
        }
        r = requests.get(BASE_URL, params=params, timeout=5)
        r.raise_for_status()
        data = r.json()

        main = data.get("weather", [{}])[0].get("main", "Clear")

        # Map API response to ML categories
        mapping = {
            "Clear": "Fine no high winds",
            "Clouds": "Fine no high winds",
            "Rain": "Raining",
            "Drizzle": "Raining",
            "Thunderstorm": "Raining",
            "Snow": "Snowing",
            "Fog": "Fog or mist",
            "Mist": "Fog or mist",
        }

        return mapping.get(main, "Fine no high winds")

    except Exception:
        # Fallback ensures API never breaks inference
        return "Fine no high winds"



