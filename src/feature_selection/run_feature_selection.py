import pandas as pd
from pathlib import Path

from src.feature_selection.probability_fs import select_probability_features
from src.feature_selection.severity_fs import select_severity_features


def main():
    print("=" * 70)
    print("PHASE 8: FEATURE SELECTION (RUNNER)")
    print("=" * 70)

    # -------------------------------------------------
    # Paths
    # -------------------------------------------------
    BASE_DIR = Path(__file__).resolve().parents[2]
    FEATURE_DIR = BASE_DIR / "data" / "processed" / "features"
    OUT_DIR = BASE_DIR / "data" / "processed" / "selected_features"
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------
    # Load datasets
    # -------------------------------------------------
    print("\n[1] Loading feature-engineered datasets...")
    train = pd.read_csv(FEATURE_DIR / "train_features.csv", low_memory=False)
    val = pd.read_csv(FEATURE_DIR / "val_features.csv", low_memory=False)
    test = pd.read_csv(FEATURE_DIR / "test_features.csv", low_memory=False)

    print("Train shape:", train.shape)
    print("Val shape  :", val.shape)
    print("Test shape :", test.shape)

    # -------------------------------------------------
    # PROBABILITY FEATURE SELECTION
    # -------------------------------------------------
    print("\n[2] Probability feature selection...")

    prob_target = (train["historical_accident_rate"] > 0).astype(int)

    prob_X_train = train.drop(
        columns=["Accident_Severity", "historical_accident_rate"],
        errors="ignore"
    )

    prob_features = select_probability_features(prob_X_train, prob_target)

    print(f"Selected probability features: {len(prob_features)}")

    train[prob_features].to_csv(OUT_DIR / "prob_train.csv", index=False)
    val[prob_features].to_csv(OUT_DIR / "prob_val.csv", index=False)
    test[prob_features].to_csv(OUT_DIR / "prob_test.csv", index=False)

    # -------------------------------------------------
    # SEVERITY FEATURE SELECTION
    # -------------------------------------------------
    print("\n[3] Severity feature selection...")

    sev_target = train["Accident_Severity"]

    sev_X_train = train.drop(
        columns=["Accident_Severity", "historical_accident_rate"],
        errors="ignore"
    )

    sev_features = select_severity_features(sev_X_train, sev_target)

    print(f"Selected severity features: {len(sev_features)}")

    train[sev_features + ["Accident_Severity"]].to_csv(
        OUT_DIR / "sev_train.csv", index=False
    )
    val[sev_features + ["Accident_Severity"]].to_csv(
        OUT_DIR / "sev_val.csv", index=False
    )
    test[sev_features + ["Accident_Severity"]].to_csv(
        OUT_DIR / "sev_test.csv", index=False
    )

    # -------------------------------------------------
    # Completion
    # -------------------------------------------------
    print("\n✔ PHASE 8 COMPLETE")
    print("Selected features saved to:", OUT_DIR)


if __name__ == "__main__":
    main()
