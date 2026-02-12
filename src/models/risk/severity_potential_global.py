import pandas as pd
from pathlib import Path

# ==================================================
# PHASE 12.2a — GLOBAL SEVERITY POTENTIAL
# ==================================================
# Computes a global severity prior from accident data
# ==================================================

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "data" / "processed"

SEV_PATH = DATA_DIR / "sev_val_scored.csv"
EXP_PATH = DATA_DIR / "probability_level_assigned.csv"

OUTPUT_PATH = DATA_DIR / "exposure_with_severity_potential.csv"

print("Loading severity (accident) dataset...")
df_sev = pd.read_csv(SEV_PATH)

print("Loading exposure (probability) dataset...")
df_exp = pd.read_csv(EXP_PATH)

# --------------------------------------------------
# Compute global severity potential
# --------------------------------------------------
global_severity = df_sev["severity_score"].mean()

print(f"Global severity potential: {global_severity:.4f}")

# --------------------------------------------------
# Assign global severity potential to all exposure rows
# --------------------------------------------------
df_exp["severity_potential"] = global_severity

# --------------------------------------------------
# Convert to severity potential level
# --------------------------------------------------
T1, T2, T3 = 0.20, 0.40, 0.65

def severity_potential_level(score: float) -> str:
    if score < T1:
        return "Low"
    elif score < T2:
        return "Moderate"
    elif score < T3:
        return "High"
    else:
        return "Severe"

df_exp["severity_potential_level"] = df_exp["severity_potential"].apply(
    severity_potential_level
)

# --------------------------------------------------
# Sanity check
# --------------------------------------------------
print("\nSeverity potential level distribution:")
print(df_exp["severity_potential_level"].value_counts())

# --------------------------------------------------
# Save
# --------------------------------------------------
df_exp.to_csv(OUTPUT_PATH, index=False)

print("\nGlobal severity potential assignment complete.")
print("Saved to:", OUTPUT_PATH)
print("PHASE 12.2a COMPLETE ✅")
