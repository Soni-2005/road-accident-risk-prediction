import joblib
import pandas as pd
from pathlib import Path

# ==================================================
# PHASE 12.1b — PROBABILITY SCORING ON SEVERITY VAL
# ==================================================

BASE_DIR = Path(__file__).resolve().parents[3]

SEV_PATH = BASE_DIR / "data" / "processed" / "sev_val_scored.csv"
MODEL_PATH = BASE_DIR / "models" / "probability" / "rf_calibrated.pkl"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "sev_val_prob_sev.csv"

print("Loading severity validation dataset...")
df = pd.read_csv(SEV_PATH)

# --------------------------------------------------
# Load probability model
# --------------------------------------------------
print("Loading calibrated probability model...")
model = joblib.load(MODEL_PATH)

# --------------------------------------------------
# Enforce feature contract from probability model
# --------------------------------------------------
PROB_FEATURES = list(model.feature_names_in_)

print("Probability features:")
for f in PROB_FEATURES:
    print("  -", f)

X_prob = df[PROB_FEATURES]

# --------------------------------------------------
# Generate probability scores
# --------------------------------------------------
print("Generating probability scores on severity validation set...")
df["probability_score"] = model.predict_proba(X_prob)[:, 1]

# --------------------------------------------------
# Sanity check
# --------------------------------------------------
print(
    f"Probability range: "
    f"{df['probability_score'].min():.4f} → {df['probability_score'].max():.4f}"
)

assert df["probability_score"].between(0, 1).all()

# --------------------------------------------------
# Save
# --------------------------------------------------
df.to_csv(OUTPUT_PATH, index=False)

print("\nSaved severity+probability dataset to:")
print(OUTPUT_PATH)
print("PHASE 12.1b COMPLETE ✅")
