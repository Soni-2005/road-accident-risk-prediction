import pandas as pd


def build_probability_features(payload: dict) -> pd.DataFrame:
    lat = float(payload["latitude"])
    lon = float(payload["longitude"])
    hour = int(payload["hour"])

    features = {
        # Spatial
        "lat_bin": int(lat * 10),
        "lon_bin": int(lon * 10),

        # Time
        "Hour": hour,
        "is_peak_hour": int(hour in [8, 9, 18, 19]),
        "is_night": int(hour < 6 or hour > 20),

        # Road defaults (NO None allowed)
        "Speed_limit": payload.get("speed_limit") or 50,
        "Road_Type": payload.get("road_type") or "Single carriageway",
        "Junction_Detail": payload.get("junction_detail") or "Not at junction",
        "Urban_or_Rural_Area": payload.get("urban_or_rural") or "Urban",
        "Light_Conditions": payload.get("light_conditions") or "Daylight",

        # Weather (CRITICAL FIX)
        "Weather_Conditions": payload.get("weather_condition") or "Fine",
    }

    df = pd.DataFrame([features])

    # 🔐 HARD SAFETY: eliminate NaN completely
    df = df.fillna({
        "Weather_Conditions": "Fine",
        "Road_Type": "Single carriageway",
        "Junction_Detail": "Not at junction",
        "Urban_or_Rural_Area": "Urban",
        "Light_Conditions": "Daylight",
        "Speed_limit": 50,
    })

    return df
