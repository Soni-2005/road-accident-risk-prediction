import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
THRESHOLD_PATH = BASE_DIR / "data" / "processed" / "risk_thresholds.json"

with open(THRESHOLD_PATH) as f:
    T = json.load(f)

MODERATE_T = T["moderate"]
HIGH_T = T["high"]
SEVERE_T = T["severe"]

def classify_risk(probability: float) -> str:
    if probability >= SEVERE_T:
        return "Severe"
    elif probability >= HIGH_T:
        return "High"
    elif probability >= MODERATE_T:
        return "Moderate"
    else:
        return "Low"
