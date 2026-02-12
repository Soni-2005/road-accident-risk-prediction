import joblib
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

# Load models ONCE
prob_model = joblib.load(
    BASE_DIR / "models/probability/rf_calibrated.pkl"
)

severity_model = joblib.load(
    BASE_DIR / "models/severity/serious_slight_rf.pkl"
)

def predict_risk_local(payload: dict) -> dict:
    """
    Local ML inference (Streamlit-safe)
    """
    hour = payload["hour"]
    weather = payload["weather_condition"]

    # 🔧 Minimal feature vector (example)
    X = np.array([[hour]])

    prob = float(prob_model.predict_proba(X)[0][1])
    severity = severity_model.predict(X)[0]

    return {
        "risk_level": "Low" if prob < 0.3 else "High",
        "probability_score": prob,
        "severity_context": "Moderate (global prior)"
    }
