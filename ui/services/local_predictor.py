import joblib
import pandas as pd
from pathlib import Path

# Resolve project root
BASE_DIR = Path(__file__).resolve().parents[2]
MODELS_DIR = BASE_DIR / "models"

# Load trained probability model (Pipeline)
prob_model = joblib.load(
    MODELS_DIR / "probability" / "rf_calibrated.pkl"
)

def normalize_road_type(rt):
    if not rt:
        return "Single carriageway"
    rt = rt.lower()
    if "dual" in rt:
        return "Dual carriageway"
    return "Single carriageway"


def normalize_light_conditions(lc):
    if not lc:
        return "Daylight"
    lc = lc.lower()
    if "dark" in lc:
        return "Darkness - lights lit"
    return "Daylight"


def normalize_weather(w):
    if not w:
        return "Fine"
    w = w.lower()
    if "rain" in w:
        return "Raining"
    if "snow" in w:
        return "Snowing"
    return "Fine"


def predict_risk_local(payload: dict) -> dict:
    """
    Local inference for Streamlit using the full feature schema
    expected by the trained pipeline.
    """

    # 🔒 Feature template — MUST match training features exactly
    features = {
    # Numeric (safe)
    "lat_bin": payload.get("lat_bin", 51.5),
    "lon_bin": payload.get("lon_bin", -0.1),
    "Hour": payload.get("hour", 12),
    "Speed_limit": payload.get("speed_limit", 30),
    "is_peak_hour": payload.get("is_peak_hour", 0),
    "is_night": payload.get("is_night", 0),

    # Categorical (MUST match training)
    "Road_Type": normalize_road_type(payload.get("road_type")),
    "Junction_Detail": payload.get("junction_detail", "Not at junction"),
    "Urban_or_Rural_Area": payload.get("urban_or_rural", 1),
    "Light_Conditions": normalize_light_conditions(payload.get("light_conditions")),
    "Weather_Conditions": normalize_weather(payload.get("weather_conditions"))
    }


    # Convert to DataFrame (CRITICAL)
    X = pd.DataFrame([features])

    # Predict probability
    prob = float(prob_model.predict_proba(X)[0][1])

    # Rule-based risk classification
    if prob < 0.30:
        risk = "Low"
    elif prob < 0.60:
        risk = "Medium"
    else:
        risk = "High"

    return {
        "risk_level": risk,
        "probability_score": round(prob, 3),
        "severity_context": "Moderate (probability-driven)",
    }
