import joblib
import numpy as np
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]
MODELS_DIR = BASE_DIR / "models"

# Load models
prob_model = joblib.load(
    MODELS_DIR / "probability" / "rf_calibrated.pkl"
)

severity_model = joblib.load(
    MODELS_DIR / "severity" / "serious_slight_rf.pkl"
)

def predict_risk_local(payload: dict) -> dict:
    hour = payload["hour"]

    # Minimal feature vector (keep simple for now)
    X = np.array([[hour]])

    prob = float(prob_model.predict_proba(X)[0][1])

    return {
        "risk_level": "Low" if prob < 0.3 else "High",
        "probability_score": prob,
        "severity_context": "Moderate (global prior)",
    }
