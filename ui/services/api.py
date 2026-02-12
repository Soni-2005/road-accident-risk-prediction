from datetime import datetime
# ui/services/api.py
import requests
from config import BACKEND_URL


def predict_risk(payload: dict) -> dict:
    return {
        "risk_level": "Low",
        "probability_score": 0.10,
        "severity_context": "Moderate (global prior)"
    }

    if response.status_code == 422:
        raise ValueError(
            f"Invalid request sent to backend: {response.text}"
        )

    if response.status_code != 200:
        raise RuntimeError(
            f"Backend error {response.status_code}: {response.text}"
        )

    return response.json()


