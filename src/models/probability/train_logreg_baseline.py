import joblib
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

from src.models.probability.evaluate_probability import (
    evaluate_probability_model
)

# -------------------------------------------------
# Main
# -------------------------------------------------
def main():
    print("=" * 72)
    print("PHASE 10.1 — PROBABILITY MODEL (LOGISTIC REGRESSION BASELINE)")
    print("Exposure-based dataset (bin × hour)")
    print("=" * 72)

    BASE_DIR = Path(__file__).resolve().parents[3]

    DATA_PATH = BASE_DIR / "data" / "processed" / "probability_exposure_dataset.csv"
    MODEL_DIR = BASE_DIR / "models" / "probability"
    REPORT_DIR = BASE_DIR / "reports" / "probability"

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------
    # Load exposure dataset
    # -------------------------------------------------
    print("\n[1] Loading probability exposure dataset...")
    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=["accident_occurred"])
    y = df["accident_occurred"]

    print("Total samples:", X.shape[0])
    print("Positive rate:", y.mean())

    # -------------------------------------------------
    # Train / validation split
    # -------------------------------------------------
    print("\n[2] Train / validation split...")
    X_train, X_val, y_train, y_val = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # -------------------------------------------------
    # Feature types
    # -------------------------------------------------
    numeric_features = [
        "lat_bin",
        "lon_bin",
        "Hour",
        "Speed_limit",
        "is_peak_hour",
        "is_night",
    ]

    categorical_features = [
        "Road_Type",
        "Junction_Detail",
        "Urban_or_Rural_Area",
        "Light_Conditions",
        "Weather_Conditions",
    ]

    # -------------------------------------------------
    # Preprocessing + model pipeline
    # -------------------------------------------------
    print("\n[3] Building preprocessing + model pipeline...")

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", "passthrough", numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore", drop="first"), categorical_features),
        ]
    )

    model = LogisticRegression(
        penalty="l2",
        solver="lbfgs",
        max_iter=1000,
        class_weight="balanced",
        random_state=42,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", model),
        ]
    )

    # -------------------------------------------------
    # Train
    # -------------------------------------------------
    print("\n[4] Training Logistic Regression baseline...")
    pipeline.fit(X_train, y_train)

    # -------------------------------------------------
    # Evaluate
    # -------------------------------------------------
    print("\n[5] Evaluating on validation set...")
    val_proba = pipeline.predict_proba(X_val)[:, 1]

    metrics = evaluate_probability_model(y_val, val_proba)

    # -------------------------------------------------
    # Save report
    # -------------------------------------------------
    report_path = REPORT_DIR / "logreg_baseline_metrics.txt"
    with open(report_path, "w") as f:
        for k, v in metrics.items():
            f.write(f"{k}: {v}\n")

    print("\nValidation Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    # -------------------------------------------------
    # Save model
    # -------------------------------------------------
    model_path = MODEL_DIR / "logreg_baseline.pkl"
    joblib.dump(pipeline, model_path)

    print("\n✔ PHASE 10.1 COMPLETE")
    print("Model saved to:", model_path)
    print("Metrics saved to:", report_path)


if __name__ == "__main__":
    main()
