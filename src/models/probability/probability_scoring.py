import joblib
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

# ==================================================
# PHASE 10.4 — PROBABILITY SCORE EXTRACTION
# ==================================================
# Generates calibrated accident probability scores
# ==================================================

def main():
    print("=" * 72)
    print("PHASE 10.4 — PROBABILITY SCORE EXTRACTION")
    print("=" * 72)

    BASE_DIR = Path(__file__).resolve().parents[3]

    DATA_PATH = BASE_DIR / "data" / "processed" / "probability_exposure_dataset.csv"
    MODEL_PATH = BASE_DIR / "models" / "probability" / "rf_calibrated.pkl"
    OUTPUT_PATH = BASE_DIR / "data" / "processed" / "prob_val_scored.csv"

    # -------------------------------------------------
    # Load data
    # -------------------------------------------------
    print("\n[1] Loading exposure dataset...")
    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=["accident_occurred"])
    y = df["accident_occurred"]

    # -------------------------------------------------
    # Match validation split used in Phase 10
    # -------------------------------------------------
    print("\n[2] Reproducing validation split...")
    _, X_val, _, y_val = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # -------------------------------------------------
    # Load calibrated model
    # -------------------------------------------------
    print("\n[3] Loading calibrated probability model...")
    model = joblib.load(MODEL_PATH)

    # -------------------------------------------------
    # Generate probability scores
    # -------------------------------------------------
    print("\n[4] Generating probability scores...")
    prob_scores = model.predict_proba(X_val)[:, 1]

    df_out = X_val.copy()
    df_out["accident_occurred"] = y_val.values
    df_out["probability_score"] = prob_scores

    # -------------------------------------------------
    # Sanity checks
    # -------------------------------------------------
    print("\nProbability score range:")
    print(
        f"{df_out['probability_score'].min():.4f} → "
        f"{df_out['probability_score'].max():.4f}"
    )

    assert df_out["probability_score"].between(0, 1).all()

    # -------------------------------------------------
    # Save
    # -------------------------------------------------
    df_out.to_csv(OUTPUT_PATH, index=False)

    print("\n✔ PHASE 10.4 COMPLETE")
    print("Saved probability-scored dataset to:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
