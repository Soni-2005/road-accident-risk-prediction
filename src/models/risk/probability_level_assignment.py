import pandas as pd
from pathlib import Path

# ==================================================
# PHASE 12.1 — PROBABILITY LEVEL ASSIGNMENT
# ==================================================
# Converts probability_score into probability_level
# ==================================================

# --------------------------------------------------
# Resolve project root (CRITICAL)
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[3]

# --------------------------------------------------
# Locate probability-scored dataset dynamically
# --------------------------------------------------
DATA_DIR = BASE_DIR / "data" / "processed"

candidate_files = [
    "probability_scored.csv",
    "prob_val_scored.csv",
    "risk_val_scored.csv",
    "accident_probability_val.csv"
]

INPUT_PATH = None
for fname in candidate_files:
    path = DATA_DIR / fname
    if path.exists():
        INPUT_PATH = path
        break

if INPUT_PATH is None:
    raise FileNotFoundError(
        "No probability-scored file found. "
        "Expected one of: " + ", ".join(candidate_files)
    )

print("Using probability file:", INPUT_PATH)

# --------------------------------------------------
# Output path
# --------------------------------------------------
OUTPUT_PATH = DATA_DIR / "probability_level_assigned.csv"

# --------------------------------------------------
# Column name (LOCKED CONTRACT)
# --------------------------------------------------
SCORE_COL = "probability_score"

# --------------------------------------------------
# Locked probability thresholds (policy-driven)
# --------------------------------------------------
P1 = 0.20
P2 = 0.40
P3 = 0.65

def assign_probability_level(score: float) -> str:
    if score < P1:
        return "Low"
    elif score < P2:
        return "Moderate"
    elif score < P3:
        return "High"
    else:
        return "Very High"

# --------------------------------------------------
# Load probability-scored data
# --------------------------------------------------
print("\nLoading probability-scored dataset...")
df = pd.read_csv(INPUT_PATH)

if SCORE_COL not in df.columns:
    raise ValueError(
        f"Column '{SCORE_COL}' not found in {INPUT_PATH.name}. "
        f"Available columns: {list(df.columns)}"
    )

# --------------------------------------------------
# Apply probability thresholds
# --------------------------------------------------
df["probability_level"] = df[SCORE_COL].apply(assign_probability_level)

# --------------------------------------------------
# Sanity checks
# --------------------------------------------------
print("\nProbability level distribution:")
print(df["probability_level"].value_counts())
print(df["probability_level"].value_counts(normalize=True))

# --------------------------------------------------
# Save output
# --------------------------------------------------
df.to_csv(OUTPUT_PATH, index=False)

print("\nProbability level assignment complete.")
print("Saved to:", OUTPUT_PATH)
print("PHASE 12.1 COMPLETE ✅")
