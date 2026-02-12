import joblib
import numpy as np
from pathlib import Path

# Resolve project root safely
BASE_DIR = Path(__file__).resolve().parents[2]
MODELS_DIR = BASE_DIR / "models"

# Load models ONCE (Streamlit cache will handle reloads)
prob_model = joblib.load(
    MODELS_DIR / "probability" / "rf_calibrated.pkl"
)

severity_model = joblib.load(
    MODELS_DIR / "severity" / "serious_slight_rf.pkl"
)


def predict_risk_local(payload: dict) -> dict:
    """
    Local inference for Streamlit (no backend).
    """

    hour = payload["hour"]

    # Minimal feature vector (placeholder — can expand later)
    X = np.array([[hour]])

    prob = float(prob_model.predict_proba(X)[0][1])

    # Simple rule-based risk (can be refined)
    if prob < 0.3:
        risk = "Low"
    elif prob < 0.6:
        risk = "Medium"
    else:
        risk = "High"

    return {
        "risk_level": risk,
        "probability_score": round(prob, 3),
        "severity_context": "Moderate (global prior)"
    }
