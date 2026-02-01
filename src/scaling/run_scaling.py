import joblib
import pandas as pd
from pathlib import Path

from src.scaling.probability_scaler import scale_probability_data
from src.scaling.severity_scaler import scale_severity_data


def main():
    print("=" * 70)
    print("PHASE 9: SCALING / NORMALIZATION")
    print("=" * 70)

    BASE_DIR = Path(__file__).resolve().parents[2]
    IN_DIR = BASE_DIR / "data" / "processed" / "selected_features"
    OUT_DIR = BASE_DIR / "data" / "processed" / "scaled_features"
    SCALER_DIR = OUT_DIR / "scalers"

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SCALER_DIR.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------
    # Load selected feature datasets
    # -------------------------------------------------
    print("\n[1] Loading selected feature datasets...")

    prob_train = pd.read_csv(IN_DIR / "prob_train.csv")
    prob_val = pd.read_csv(IN_DIR / "prob_val.csv")
    prob_test = pd.read_csv(IN_DIR / "prob_test.csv")

    sev_train = pd.read_csv(IN_DIR / "sev_train.csv")
    sev_val = pd.read_csv(IN_DIR / "sev_val.csv")
    sev_test = pd.read_csv(IN_DIR / "sev_test.csv")

    # -------------------------------------------------
    # Probability scaling
    # -------------------------------------------------
    print("\n[2] Scaling probability features...")

    prob_train_s, prob_val_s, prob_test_s, prob_scaler, prob_scaled_cols = (
        scale_probability_data(prob_train, prob_val, prob_test)
    )

    prob_train_s.to_csv(OUT_DIR / "prob_train_scaled.csv", index=False)
    prob_val_s.to_csv(OUT_DIR / "prob_val_scaled.csv", index=False)
    prob_test_s.to_csv(OUT_DIR / "prob_test_scaled.csv", index=False)

    joblib.dump(prob_scaler, SCALER_DIR / "prob_scaler.pkl")

    print(f"Scaled probability columns: {len(prob_scaled_cols)}")

    # -------------------------------------------------
    # Severity scaling
    # -------------------------------------------------
    print("\n[3] Scaling severity features...")

    sev_train_s, sev_val_s, sev_test_s, sev_scaler, sev_scaled_cols = (
        scale_severity_data(sev_train, sev_val, sev_test)
    )

    sev_train_s.to_csv(OUT_DIR / "sev_train_scaled.csv", index=False)
    sev_val_s.to_csv(OUT_DIR / "sev_val_scaled.csv", index=False)
    sev_test_s.to_csv(OUT_DIR / "sev_test_scaled.csv", index=False)

    joblib.dump(sev_scaler, SCALER_DIR / "sev_scaler.pkl")

    print(f"Scaled severity columns: {len(sev_scaled_cols)}")

    print("\n✔ PHASE 9 COMPLETE")
    print("Scaled datasets saved to:", OUT_DIR)


if __name__ == "__main__":
    main()
