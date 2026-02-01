import requests
from datetime import datetime
from config import BACKEND_URL


def predict_risk(lat: float, lon: float) -> dict:
    payload = {
        "latitude": lat,
        "longitude": lon,
        "hour": datetime.now().hour,
        "speed_limit": 40,
        "road_type": "Single carriageway",
        "junction_detail": "Not at junction",
        "urban_or_rural": "Urban",
        "light_conditions": "Daylight",
    }

    response = requests.post(
        f"{BACKEND_URL}/predict-risk",
        json=payload,
        timeout=10,
    )

    response.raise_for_status()
    return response.json()
