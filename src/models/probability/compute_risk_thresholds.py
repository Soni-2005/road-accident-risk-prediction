import json
import joblib
import pandas as pd
import numpy as np
from pathlib import Path

def main():
    print("=" * 72)
    print("PHASE 10.3b — RISK THRESHOLD COMPUTATION (QUANTILE-BASED)")
    print("=" * 72)

    BASE_DIR = Path(__file__).resolve().parents[3]

    DATA_PATH = BASE_DIR / "data" / "processed" / "probability_exposure_dataset.csv"
    MODEL_PATH = BASE_DIR / "models" / "probability" / "rf_calibrated.pkl"
    OUTPUT_PATH = BASE_DIR / "data" / "processed" / "risk_thresholds.json"

    # -------------------------------------------------
    # Load data & model
    # -------------------------------------------------
    df = pd.read_csv(DATA_PATH)
    model = joblib.load(MODEL_PATH)

    X = df.drop(columns=["accident_occurred"])

    print("\n[1] Generating calibrated probabilities...")
    probs = model.predict_proba(X)[:, 1]

    # -------------------------------------------------
    # Quantile thresholds
    # -------------------------------------------------
    thresholds = {
        "moderate": float(np.quantile(probs, 0.50)),
        "high": float(np.quantile(probs, 0.75)),
        "severe": float(np.quantile(probs, 0.90)),
    }

    # -------------------------------------------------
    # Save
    # -------------------------------------------------
    with open(OUTPUT_PATH, "w") as f:
        json.dump(thresholds, f, indent=4)

    print("\n✔ Risk thresholds computed & frozen:")
    for k, v in thresholds.items():
        print(f"{k.upper():>8}: {v:.4f}")

    print("\nSaved to:", OUTPUT_PATH)

if __name__ == "__main__":
    main()
