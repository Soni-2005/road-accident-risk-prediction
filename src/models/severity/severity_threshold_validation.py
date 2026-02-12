import pandas as pd
from pathlib import Path

# ==================================================
# PHASE 11.3c — SEVERITY THRESHOLDING
# ==================================================
# Converts severity_score into severity_level
# ==================================================

BASE_DIR = Path(__file__).resolve().parents[3]

INPUT_PATH = BASE_DIR / "data" / "processed" / "sev_val_scored.csv"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "sev_val_severity_level.csv"

SCORE_COL = "severity_score"

# --------------------------------------------------
# Locked thresholds (policy-driven)
# --------------------------------------------------
T1 = 0.20
T2 = 0.40
T3 = 0.65

def assign_severity_level(score: float) -> str:
    if score < T1:
        return "Low"
    elif score < T2:
        return "Moderate"
    elif score < T3:
        return "High"
    else:
        return "Severe"

# --------------------------------------------------
# Load scored data
# --------------------------------------------------
df = pd.read_csv(INPUT_PATH)

# --------------------------------------------------
# Apply severity thresholds
# --------------------------------------------------
df["severity_level"] = df[SCORE_COL].apply(assign_severity_level)

# --------------------------------------------------
# Sanity check
# --------------------------------------------------
print("Severity level distribution:")
print(df["severity_level"].value_counts())
print(df["severity_level"].value_counts(normalize=True))

# --------------------------------------------------
# Save output
# --------------------------------------------------
df.to_csv(OUTPUT_PATH, index=False)

print("\nSeverity thresholding complete.")
print("Saved to:", OUTPUT_PATH)
print("PHASE 11.3c COMPLETE ✅")
