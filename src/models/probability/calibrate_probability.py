import joblib
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import brier_score_loss, roc_auc_score

# -------------------------------------------------
# Main
# -------------------------------------------------
def main():
    print("=" * 72)
    print("PHASE 10.3 — PROBABILITY CALIBRATION")
    print("Random Forest → calibrated probabilities")
    print("=" * 72)

    BASE_DIR = Path(__file__).resolve().parents[3]

    DATA_PATH = BASE_DIR / "data" / "processed" / "probability_exposure_dataset.csv"
    MODEL_PATH = BASE_DIR / "models" / "probability" / "rf_baseline.pkl"
    OUTPUT_DIR = BASE_DIR / "models" / "probability"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------
    # Load data
    # -------------------------------------------------
    print("\n[1] Loading exposure dataset...")
    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=["accident_occurred"])
    y = df["accident_occurred"]

    X_train, X_val, y_train, y_val = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # -------------------------------------------------
    # Load base model
    # -------------------------------------------------
    print("\n[2] Loading Random Forest baseline...")
    base_model = joblib.load(MODEL_PATH)

    # -------------------------------------------------
    # Baseline probability
    # -------------------------------------------------
    print("\n[3] Evaluating uncalibrated probabilities...")
    uncal_proba = base_model.predict_proba(X_val)[:, 1]

    base_brier = brier_score_loss(y_val, uncal_proba)
    base_auc = roc_auc_score(y_val, uncal_proba)

    print(f"Uncalibrated Brier Score: {base_brier:.4f}")
    print(f"Uncalibrated ROC-AUC   : {base_auc:.4f}")

    # -------------------------------------------------
    # Platt Scaling (Sigmoid)
    # -------------------------------------------------
    print("\n[4] Applying Platt Scaling (sigmoid)...")
    platt = CalibratedClassifierCV(
        estimator=base_model,
        method="sigmoid",
        cv="prefit"
    )
    platt.fit(X_val, y_val)

    platt_proba = platt.predict_proba(X_val)[:, 1]
    platt_brier = brier_score_loss(y_val, platt_proba)
    platt_auc = roc_auc_score(y_val, platt_proba)

    print(f"Platt Brier Score: {platt_brier:.4f}")
    print(f"Platt ROC-AUC   : {platt_auc:.4f}")

    # -------------------------------------------------
    # Isotonic Regression
    # -------------------------------------------------
    print("\n[5] Applying Isotonic Regression...")
    iso = CalibratedClassifierCV(
        estimator=base_model,
        method="isotonic",
        cv="prefit"
    )
    iso.fit(X_val, y_val)

    iso_proba = iso.predict_proba(X_val)[:, 1]
    iso_brier = brier_score_loss(y_val, iso_proba)
    iso_auc = roc_auc_score(y_val, iso_proba)

    print(f"Isotonic Brier Score: {iso_brier:.4f}")
    print(f"Isotonic ROC-AUC   : {iso_auc:.4f}")

    # -------------------------------------------------
    # Select best calibration
    # -------------------------------------------------
    print("\n[6] Selecting best calibrated model...")

    results = {
        "platt": (platt, platt_brier),
        "isotonic": (iso, iso_brier),
    }

    best_method = min(results, key=lambda k: results[k][1])
    best_model, best_brier = results[best_method]

    print(f"Best calibration method: {best_method}")
    print(f"Best Brier Score       : {best_brier:.4f}")

    # -------------------------------------------------
    # Save calibrated model
    # -------------------------------------------------
    output_path = OUTPUT_DIR / "rf_calibrated.pkl"
    joblib.dump(best_model, output_path)

    print("\n✔ PHASE 10.3 COMPLETE")
    print("Calibrated model saved to:", output_path)


if __name__ == "__main__":
    main()
