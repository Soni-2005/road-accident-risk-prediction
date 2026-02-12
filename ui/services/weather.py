# ==================================================
# UI SERVICE — WEATHER
# Phase 13.5 / 14.3
# ==================================================

import requests
from config import BACKEND_URL
# ui/services/weather.py
import os
from config import BACKEND_URL
from datetime import datetime


OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "").strip()
def get_weather(latitude: float, longitude: float) -> dict:
    """
    Fetch current weather directly from OpenWeather API.
    """

    if not OPENWEATHER_API_KEY:
        return {
            "condition": "Unavailable",
            "temperature": None,
            "humidity": None,
            "wind_speed": None,
            "error": "OPENWEATHER_API_KEY not set",
        }

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    try:
        response = requests.get(
            BASE_URL,
            params={
                "lat": latitude,
                "lon": longitude,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric",
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "condition": data["weather"][0]["main"],
            "source": "current",
        }

    except Exception as e:
        return {
            "condition": "Unavailable",
            "temperature": None,
            "humidity": None,
            "wind_speed": None,
            "error": str(e),
        }
# ui/services/weather.py

def get_forecast_weather(latitude, longitude, start_timestamp, end_timestamp):
    """
    Fetch forecast weather for a given location and time window.
    """

    if not OPENWEATHER_API_KEY:
        raise RuntimeError("OPENWEATHER_API_KEY not set in environment")

    BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    start_dt = datetime.fromisoformat(start_timestamp)
    end_dt = datetime.fromisoformat(end_timestamp)

    forecasts = []

    for entry in data.get("list", []):
        forecast_time = datetime.utcfromtimestamp(entry["dt"])

        if start_dt <= forecast_time <= end_dt:
            forecasts.append(entry)

    if not forecasts:
        return None

    avg_temp = sum(f["main"]["temp"] for f in forecasts) / len(forecasts)
    avg_wind = sum(f["wind"]["speed"] for f in forecasts) / len(forecasts)
    condition = forecasts[0]["weather"][0]["main"]

    return {
    "temperature": round(avg_temp, 2),
    "humidity": None,              # ❗ forecast API doesn’t provide reliable humidity
    "wind_speed": round(avg_wind, 2),
    "condition": condition,
    "source": "forecast",
}
