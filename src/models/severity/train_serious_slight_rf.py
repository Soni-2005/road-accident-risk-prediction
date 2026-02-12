import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    f1_score,
    balanced_accuracy_score,
)

def main():
    print("=" * 76)
    print("PHASE 11.2b — SERIOUS vs SLIGHT SEVERITY MODEL")
    print("Random Forest | Macro-F1 & Serious Recall priority")
    print("=" * 76)

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
    # Load datasets
    # -------------------------------------------------
    print("\n[1] Loading scaled severity datasets...")

    train = pd.read_csv(DATA_DIR / "sev_train_scaled.csv")
    val = pd.read_csv(DATA_DIR / "sev_val_scaled.csv")
    test = pd.read_csv(DATA_DIR / "sev_test_scaled.csv")

    TARGET = "Accident_Severity"

    # -------------------------------------------------
    # Filter NON-FATAL only (Severity 2 & 3)
    # -------------------------------------------------
    train = train[train[TARGET].isin([2, 3])]
    val = val[val[TARGET].isin([2, 3])]
    test = test[test[TARGET].isin([2, 3])]

    print("Train size:", train.shape)
    print("Val size  :", val.shape)
    print("Test size :", test.shape)

    # -------------------------------------------------
    # Binary target: Serious = 1, Slight = 0
    # -------------------------------------------------
    def build_xy(df):
        X = df.drop(columns=[TARGET]).select_dtypes(include=["number"])
        y = (df[TARGET] == 2).astype(int)
        return X, y

    X_train, y_train = build_xy(train)
    X_val, y_val = build_xy(val)
    X_test, y_test = build_xy(test)

    # Safety cleanup
    X_train = X_train.replace([np.inf, -np.inf], np.nan).fillna(0)
    X_val = X_val.replace([np.inf, -np.inf], np.nan).fillna(0)
    X_test = X_test.replace([np.inf, -np.inf], np.nan).fillna(0)

    print("\nClass distribution (train):")
    print(y_train.value_counts(normalize=True))

    # -------------------------------------------------
    # Train Random Forest
    # -------------------------------------------------
    print("\n[2] Training Random Forest (balanced)...")

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=15,
        min_samples_leaf=10,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    # -------------------------------------------------
    # Evaluate on validation
    # -------------------------------------------------
    print("\n[3] Evaluating on validation set...")

    val_pred = model.predict(X_val)

    cm = confusion_matrix(y_val, val_pred)
    macro_f1 = f1_score(y_val, val_pred, average="macro")
    bal_acc = balanced_accuracy_score(y_val, val_pred)

    print("\nConfusion Matrix (rows=true, cols=pred):")
    print("Labels: [Slight (0), Serious (1)]")
    print(cm)

    print(f"\nMacro F1-score      : {macro_f1:.4f}")
    print(f"Balanced Accuracy   : {bal_acc:.4f}")

    report = classification_report(y_val, val_pred, digits=4)
    print("\nClassification Report:")
    print(report)

    # -------------------------------------------------
    # Save artifacts
    # -------------------------------------------------
    model_path = MODEL_DIR / "serious_slight_rf.pkl"
    report_path = REPORT_DIR / "serious_slight_rf_report.txt"

    joblib.dump(model, model_path)

    with open(report_path, "w") as f:
        f.write("Confusion Matrix [Slight, Serious]:\n")
        f.write(str(cm))
        f.write("\n\n")
        f.write(f"Macro F1-score: {macro_f1:.4f}\n")
        f.write(f"Balanced Accuracy: {bal_acc:.4f}\n\n")
        f.write(report)

    print("\n✔ PHASE 11.2b COMPLETE")
    print("Model saved to:", model_path)
    print("Report saved to:", report_path)

if __name__ == "__main__":
    main()
