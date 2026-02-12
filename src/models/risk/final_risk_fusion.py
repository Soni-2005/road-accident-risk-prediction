import pandas as pd
from pathlib import Path

# ==================================================
# PHASE 12.2b — FINAL RISK FUSION
# ==================================================
# Risk driven by probability with global severity prior
# ==================================================

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "data" / "processed"

INPUT_PATH = DATA_DIR / "probability_level_assigned.csv"
OUTPUT_PATH = DATA_DIR / "final_risk_output.csv"

print("Loading probability-level dataset...")
df = pd.read_csv(INPUT_PATH)

# --------------------------------------------------
# Final risk logic (LOCKED)
# --------------------------------------------------
def assign_risk(prob_level: str) -> str:
    if prob_level == "Very High":
        return "Severe"
    elif prob_level == "High":
        return "High"
    elif prob_level == "Moderate":
        return "Moderate"
    else:
        return "Low"

df["risk_level"] = df["probability_level"].apply(assign_risk)

# --------------------------------------------------
# Sanity check
# --------------------------------------------------
print("\nFinal risk level distribution:")
print(df["risk_level"].value_counts())
print(df["risk_level"].value_counts(normalize=True))

# --------------------------------------------------
# Save
# --------------------------------------------------
df.to_csv(OUTPUT_PATH, index=False)

print("\nFinal risk fusion complete.")
print("Saved to:", OUTPUT_PATH)
print("PHASE 12 COMPLETE ✅")
