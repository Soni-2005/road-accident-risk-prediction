from datetime import datetime
# ui/services/api.py
import requests
from config import BACKEND_URL


def predict_risk(payload: dict) -> dict:
    response = requests.post(
        f"{BACKEND_URL}/predict-risk",
        json=payload,
        timeout=10,
    )

    if response.status_code == 422:
        raise ValueError(
            f"Invalid request sent to backend: {response.text}"
        )

    if response.status_code != 200:
        raise RuntimeError(
            f"Backend error {response.status_code}: {response.text}"
        )

    return response.json()


