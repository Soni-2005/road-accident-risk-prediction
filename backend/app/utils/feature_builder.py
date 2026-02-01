# --------------------------------------------------
# 2. backend/app/utils/feature_builder.py (UPDATED)
# --------------------------------------------------
import pandas as pd
from backend.app.services.weather import fetch_weather


def build_probability_features(payload: dict) -> pd.DataFrame:
    lat = payload["latitude"]
    lon = payload["longitude"]
    hour = payload["hour"]

    # Fetch weather dynamically
    weather_condition = fetch_weather(lat, lon)

    features = {
        "lat_bin": int(lat * 10),
        "lon_bin": int(lon * 10),
        "Hour": hour,
        "Speed_limit": payload["speed_limit"],

        "Road_Type": payload["road_type"],
        "Junction_Detail": payload["junction_detail"],
        "Urban_or_Rural_Area": payload["urban_or_rural"],
        "Light_Conditions": payload["light_conditions"],
        "Weather_Conditions": weather_condition,

        "is_peak_hour": int(hour in [8, 9, 18, 19]),
        "is_night": int(hour < 6 or hour > 20),
    }

    return pd.DataFrame([features])
