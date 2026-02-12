import pandas as pd
import joblib
from pathlib import Path

# ==================================================
# PHASE 11.3a — SEVERITY SCORE EXTRACTION (FINAL)
# ==================================================

# --------------------------------------------------
# Resolve project root
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[3]
print("Resolved BASE_DIR:", BASE_DIR)

# --------------------------------------------------
# Paths
# --------------------------------------------------
MODEL_PATH = BASE_DIR / "models" / "severity" / "serious_slight_rf.pkl"

SCALED_DIR = BASE_DIR / "data" / "processed" / "scaled_features"

VAL_DATA_PATH = SCALED_DIR / "sev_val_scaled.csv"
TEST_DATA_PATH = SCALED_DIR / "sev_test_scaled.csv"

OUTPUT_VAL_PATH = BASE_DIR / "data" / "processed" / "sev_val_scored.csv"
OUTPUT_TEST_PATH = BASE_DIR / "data" / "processed" / "sev_test_scored.csv"

TARGET_COL = "Accident_Severity"

# --------------------------------------------------
# Load model
# --------------------------------------------------
print("\nLoading severity model...")
print("Model path:", MODEL_PATH)

model = joblib.load(MODEL_PATH)
print("Model loaded successfully.")

# --------------------------------------------------
# 🔑 LOAD FEATURE CONTRACT DIRECTLY FROM MODEL
# --------------------------------------------------
print("\nExtracting feature contract from trained model...")

TRAINED_FEATURES = list(model.feature_names_in_)

print(f"Number of trained features: {len(TRAINED_FEATURES)}")
print("Trained features:")
for f in TRAINED_FEATURES:
    print("  -", f)

# --------------------------------------------------
# Load datasets
# --------------------------------------------------
print("\nLoading validation and test datasets...")
print("Validation path:", VAL_DATA_PATH)
print("Test path      :", TEST_DATA_PATH)

df_val = pd.read_csv(VAL_DATA_PATH)
df_test = pd.read_csv(TEST_DATA_PATH)

print(f"Validation shape: {df_val.shape}")
print(f"Test shape      : {df_test.shape}")

# --------------------------------------------------
# Enforce feature contract (THIS IS THE FIX)
# --------------------------------------------------
X_val = df_val[TRAINED_FEATURES]
X_test = df_test[TRAINED_FEATURES]

# --------------------------------------------------
# Generate severity scores
# --------------------------------------------------
print("\nGenerating severity scores...")

val_severity_score = model.predict_proba(X_val)[:, 1]
test_severity_score = model.predict_proba(X_test)[:, 1]

# --------------------------------------------------
# Attach severity score
# --------------------------------------------------
df_val["severity_score"] = val_severity_score
df_test["severity_score"] = test_severity_score

# --------------------------------------------------
# Sanity checks
# --------------------------------------------------
print("\nSeverity score sanity check:")
print(
    f"Validation range: "
    f"{df_val['severity_score'].min():.4f} → {df_val['severity_score'].max():.4f}"
)
print(
    f"Test range      : "
    f"{df_test['severity_score'].min():.4f} → {df_test['severity_score'].max():.4f}"
)

assert df_val["severity_score"].between(0, 1).all()
assert df_test["severity_score"].between(0, 1).all()

print("Severity scores are valid probabilities.")

# --------------------------------------------------
# Save outputs
# --------------------------------------------------
df_val.to_csv(OUTPUT_VAL_PATH, index=False)
df_test.to_csv(OUTPUT_TEST_PATH, index=False)

print("\nScored datasets saved:")
print("Validation →", OUTPUT_VAL_PATH)
print("Test       →", OUTPUT_TEST_PATH)

print("\nPHASE 11.3a COMPLETE ✅")
