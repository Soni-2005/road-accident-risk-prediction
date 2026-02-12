import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    recall_score,
    precision_score,
    roc_auc_score,
)

def main():
    print("=" * 72)
    print("PHASE 11.2a — FATAL vs NON-FATAL SEVERITY MODEL")
    print("Logistic Regression baseline | Fatal recall is priority")
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

    TARGET = "Accident_Severity"

    # -------------------------------------------------
    # Build binary target: Fatal vs Non-Fatal
    # -------------------------------------------------
    def make_binary(df):
        X = df.drop(columns=[TARGET]).select_dtypes(include=["number"])
        y = (df[TARGET] == 1).astype(int)  # 1 = Fatal, 0 = Non-Fatal
        return X, y

    X_train, y_train = make_binary(train)
    X_val, y_val = make_binary(val)
    X_test, y_test = make_binary(test)

    print("Train shape:", X_train.shape, "| Fatal rate:", y_train.mean())
    print("Val shape  :", X_val.shape,   "| Fatal rate:", y_val.mean())
    print("Test shape :", X_test.shape,  "| Fatal rate:", y_test.mean())

    # Safety: ensure finite
    X_train = X_train.replace([np.inf, -np.inf], np.nan).fillna(0)
    X_val   = X_val.replace([np.inf, -np.inf], np.nan).fillna(0)
    X_test  = X_test.replace([np.inf, -np.inf], np.nan).fillna(0)

    # -------------------------------------------------
    # Train Logistic Regression
    # -------------------------------------------------
    print("\n[2] Training Logistic Regression (class_weight=balanced)...")

    model = LogisticRegression(
        penalty="l2",
        solver="lbfgs",
        max_iter=2000,
        class_weight="balanced",
        random_state=42,
        n_jobs=None
    )

    model.fit(X_train, y_train)

    # -------------------------------------------------
    # Evaluate on validation
    # -------------------------------------------------
    print("\n[3] Evaluating on validation set...")

    val_proba = model.predict_proba(X_val)[:, 1]
    val_pred = (val_proba >= 0.5).astype(int)  # default threshold

    cm = confusion_matrix(y_val, val_pred)
    fatal_recall = recall_score(y_val, val_pred, zero_division=0)
    fatal_precision = precision_score(y_val, val_pred, zero_division=0)
    roc = roc_auc_score(y_val, val_proba)

    print("\nConfusion Matrix (rows=true, cols=pred):")
    print("Labels: [Non-Fatal, Fatal]")
    print(cm)

    print(f"\nFatal Recall   : {fatal_recall:.4f}")
    print(f"Fatal Precision: {fatal_precision:.4f}")
    print(f"ROC-AUC        : {roc:.4f}")

    report = classification_report(y_val, val_pred, digits=4)
    print("\nClassification Report:")
    print(report)

    # -------------------------------------------------
    # Save artifacts
    # -------------------------------------------------
    model_path = MODEL_DIR / "fatal_logreg_baseline.pkl"
    report_path = REPORT_DIR / "fatal_logreg_baseline_report.txt"

    joblib.dump(model, model_path)

    with open(report_path, "w") as f:
        f.write("Confusion Matrix [Non-Fatal, Fatal]:\n")
        f.write(str(cm))
        f.write("\n\n")
        f.write(f"Fatal Recall: {fatal_recall:.4f}\n")
        f.write(f"Fatal Precision: {fatal_precision:.4f}\n")
        f.write(f"ROC-AUC: {roc:.4f}\n\n")
        f.write(report)

    print("\n✔ PHASE 11.2a COMPLETE")
    print("Model saved to:", model_path)
    print("Report saved to:", report_path)

if __name__ == "__main__":
    main()
