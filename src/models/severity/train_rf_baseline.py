import joblib
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    recall_score
)

def main():
    print("=" * 72)
    print("PHASE 11.1 — SEVERITY MODEL (RANDOM FOREST BASELINE)")
    print("Fatal recall is the priority metric")
    print("=" * 72)

    # -------------------------------------------------
    # Paths
    # -------------------------------------------------
    BASE_DIR = Path(__file__).resolve().parents[3]

    DATA_DIR = BASE_DIR / "data" / "processed" / "scaled_features"
    MODEL_DIR = BASE_DIR / "models" / "severity"
    REPORT_DIR = BASE_DIR / "reports" / "severity"

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------
    # Load data
    # -------------------------------------------------
    print("\n[1] Loading scaled severity datasets...")

    train = pd.read_csv(DATA_DIR / "sev_train_scaled.csv")
    val = pd.read_csv(DATA_DIR / "sev_val_scaled.csv")
    test = pd.read_csv(DATA_DIR / "sev_test_scaled.csv")

    # -------------------------------------------------
    # Split features / target
    # -------------------------------------------------
    TARGET_COL = "Accident_Severity"

    # Keep only numeric features (safety enforcement)
    X_train = train.drop(columns=[TARGET_COL]).select_dtypes(include=["number"])
    y_train = train[TARGET_COL]

    X_val = val.drop(columns=[TARGET_COL]).select_dtypes(include=["number"])
    y_val = val[TARGET_COL]

    X_test = test.drop(columns=[TARGET_COL]).select_dtypes(include=["number"])
    y_test = test[TARGET_COL]

    print("\nNumeric feature count:", X_train.shape[1])

    print("Train shape:", X_train.shape)
    print("Validation shape:", X_val.shape)
    print("Test shape:", X_test.shape)

    # -------------------------------------------------
    # Train Random Forest
    # -------------------------------------------------
    print("\n[2] Training Random Forest (balanced_subsample)...")

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_leaf=2,
        class_weight="balanced_subsample",
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    # -------------------------------------------------
    # Evaluate on validation set
    # -------------------------------------------------
    print("\n[3] Evaluating on validation set...")

    y_val_pred = model.predict(X_val)

    cm = confusion_matrix(y_val, y_val_pred, labels=[1, 2, 3])
    fatal_recall = recall_score(
        y_val,
        y_val_pred,
        labels=[1],
        average="macro",
        zero_division=0
    )

    print("\nConfusion Matrix (rows=true, cols=pred):")
    print("Labels: [Fatal, Serious, Slight]")
    print(cm)

    print(f"\nFatal Recall (severity=1): {fatal_recall:.4f}")

    report = classification_report(
        y_val,
        y_val_pred,
        digits=4
    )

    print("\nClassification Report:")
    print(report)

    # -------------------------------------------------
    # Save artifacts
    # -------------------------------------------------
    model_path = MODEL_DIR / "rf_severity_baseline.pkl"
    report_path = REPORT_DIR / "rf_severity_baseline_report.txt"

    joblib.dump(model, model_path)

    with open(report_path, "w") as f:
        f.write("Confusion Matrix (Fatal, Serious, Slight):\n")
        f.write(str(cm))
        f.write("\n\n")
        f.write(f"Fatal Recall: {fatal_recall:.4f}\n\n")
        f.write(report)

    print("\n✔ PHASE 11.1 COMPLETE")
    print("Model saved to:", model_path)
    print("Report saved to:", report_path)

if __name__ == "__main__":
    main()
