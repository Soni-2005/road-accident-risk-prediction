# ==================================================
# UI SERVICE — WEATHER
# Phase 13.5 / 14.3
# ==================================================

import requests
from config import BACKEND_URL


def get_weather(latitude: float, longitude: float) -> dict:
    """
    Fetch live weather information from backend.

    Returns a normalized weather dictionary for UI rendering.
    """

    try:
        response = requests.get(
            f"{BACKEND_URL}/weather",
            params={
                "lat": latitude,
                "lon": longitude,
            },
            timeout=5,
        )
        response.raise_for_status()
        return response.json()

    except Exception as e:
        # Graceful fallback (never crash UI)
        return {
            "condition": "Unavailable",
            "temperature": None,
            "humidity": None,
            "wind_speed": None,
            "error": str(e),
        }
