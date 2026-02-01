from pathlib import Path
import json
import os

BASE_DIR = Path(__file__).resolve().parents[2]

# -----------------------------
# Model paths
# -----------------------------
PROB_MODEL_PATH = BASE_DIR / "models" / "probability" / "rf_calibrated.pkl"

# -----------------------------
# Thresholds
# -----------------------------
THRESHOLD_PATH = BASE_DIR / "data" / "processed" / "risk_thresholds.json"

with open(THRESHOLD_PATH) as f:
    RISK_THRESHOLDS = json.load(f)

MODERATE_T = RISK_THRESHOLDS["moderate"]
HIGH_T = RISK_THRESHOLDS["high"]
SEVERE_T = RISK_THRESHOLDS["severe"]

# Weather API Key (used in Phase 13.5)
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

if WEATHER_API_KEY is None:
    raise RuntimeError(
        "WEATHER_API_KEY not found. "
        "Please set it as an environment variable."
    )