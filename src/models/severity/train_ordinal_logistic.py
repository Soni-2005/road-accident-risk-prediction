"""
ABANDONED APPROACH:
Ordinal Logistic Regression using statsmodels.
Reason: numerical instability + lack of sample-weight support
Replaced by two-stage severity modeling.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    recall_score
)
from statsmodels.miscmodels.ordinal_model import OrderedModel

def main():
    print("=" * 72)
    print("PHASE 11.2 — SEVERITY MODEL (ORDINAL LOGISTIC REGRESSION)")
    print("Fatal recall is the priority metric")
    print("=" * 72)

    # -------------------------------------------------
    # Paths
    # -------------------------------------------------
    BASE_DIR = Path(__file__).resolve().parents[3]
    DATA_DIR = BASE_DIR / "data" / "processed" / "scaled_features"
    REPORT_DIR = BASE_DIR / "reports" / "severity"

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------
    # Load data
    # -------------------------------------------------
  
    train = pd.read_csv(DATA_DIR / "sev_train_scaled.csv")
    val = pd.read_csv(DATA_DIR / "sev_val_scaled.csv")

    TARGET = "Accident_Severity"

    X_train = train.drop(columns=[TARGET]).select_dtypes(include=["number"])
    y_train = train[TARGET].astype(int)

    X_val = val.drop(columns=[TARGET]).select_dtypes(include=["number"])
    y_val = val[TARGET].astype(int)

    # -------------------------------------------------
    # Numeric sanitation (REQUIRED for statsmodels)
    # -------------------------------------------------
    X_train = X_train.replace([np.inf, -np.inf], np.nan)
    X_val = X_val.replace([np.inf, -np.inf], np.nan)

    X_train = X_train.fillna(0)
    X_val = X_val.fillna(0)

    # Optional safety check
    assert np.isfinite(X_train.values).all()
    assert np.isfinite(X_val.values).all()


    X_val = val.drop(columns=[TARGET]).select_dtypes(include=["number"])
    y_val = val[TARGET].astype(int)

    print("Train shape:", X_train.shape)
    print("Validation shape:", X_val.shape)

    # -------------------------------------------------
    # Sample weights (handle imbalance)
    # -------------------------------------------------
    print("\n[2] Computing class weights...")

    class_counts = y_train.value_counts().sort_index()
    class_weights = class_counts.max() / class_counts

    sample_weights = y_train.map(class_weights)

    print("Class weights:")
    print(class_weights)

    # -------------------------------------------------
    # Train Ordinal Logistic Model
    # -------------------------------------------------
    print("\n[3] Training ordinal logistic regression...")

    model = OrderedModel(
        y_train,
        X_train,
        distr="logit"
    )

    result = model.fit(
        method="bfgs",
        maxiter=1000,
        disp=False,
        weights=sample_weights
    )

    # -------------------------------------------------
    # Predict on validation set
    # -------------------------------------------------
    print("\n[4] Evaluating on validation set...")

    val_probs = result.model.predict(result.params, X_val)
    y_val_pred = val_probs.idxmax(axis=1).astype(int)

    # -------------------------------------------------
    # Metrics
    # -------------------------------------------------
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
    # Save report
    # -------------------------------------------------
    report_path = REPORT_DIR / "ordinal_logistic_severity_report.txt"
    with open(report_path, "w") as f:
        f.write("Confusion Matrix (Fatal, Serious, Slight):\n")
        f.write(str(cm))
        f.write("\n\n")
        f.write(f"Fatal Recall: {fatal_recall:.4f}\n\n")
        f.write(report)

    print("\n✔ PHASE 11.2 COMPLETE")
    print("Report saved to:", report_path)

if __name__ == "__main__":
    main()
