import pandas as pd
from pathlib import Path

# ==================================================
# PHASE 12.2 — RISK FUSION USING DECISION MATRIX
# ==================================================

# --------------------------------------------------
# Resolve project root
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "data" / "processed"

# --------------------------------------------------
# Locate probability-level dataset
# --------------------------------------------------
PROB_PATH = DATA_DIR / "probability_level_assigned.csv"
if not PROB_PATH.exists():
    raise FileNotFoundError(
        f"Probability-level file not found: {PROB_PATH}"
    )

print("Using probability-level file:", PROB_PATH)

# --------------------------------------------------
# Locate severity-level dataset dynamically
# --------------------------------------------------
severity_candidates = [
    "sev_val_severity_level.csv",
    "sev_severity_level.csv",
    "severity_level_val.csv",
    "severity_level.csv",
]

SEV_PATH = None
for fname in severity_candidates:
    path = DATA_DIR / fname
    if path.exists():
        SEV_PATH = path
        break

if SEV_PATH is None:
    raise FileNotFoundError(
        "No severity-level file found. Expected one of: "
        + ", ".join(severity_candidates)
    )

print("Using severity-level file:", SEV_PATH)

# --------------------------------------------------
# Load datasets
# --------------------------------------------------
df_prob = pd.read_csv(PROB_PATH)
df_sev = pd.read_csv(SEV_PATH)

# --------------------------------------------------
# Validate required columns
# --------------------------------------------------
required_prob_cols = {"probability_level"}
required_sev_cols = {"severity_level"}

if not required_prob_cols.issubset(df_prob.columns):
    raise ValueError(
        f"Missing columns in probability dataset. "
        f"Found: {list(df_prob.columns)}"
    )

if not required_sev_cols.issubset(df_sev.columns):
    raise ValueError(
        f"Missing columns in severity dataset. "
        f"Found: {list(df_sev.columns)}"
    )

# --------------------------------------------------
# Align datasets (validation split, same order)
# --------------------------------------------------
if len(df_prob) != len(df_sev):
    raise ValueError(
        "Probability and severity datasets have different lengths. "
        "They must correspond to the same validation split."
    )

df = df_prob.copy()
df["severity_level"] = df_sev["severity_level"].values

# --------------------------------------------------
# Risk fusion matrix (LOCKED POLICY)
# --------------------------------------------------
RISK_MATRIX = {
    ("Low", "Low"): "Low",
    ("Low", "Moderate"): "Low",
    ("Low", "High"): "Moderate",
    ("Low", "Very High"): "Moderate",

    ("Moderate", "Low"): "Low",
    ("Moderate", "Moderate"): "Moderate",
    ("Moderate", "High"): "High",
    ("Moderate", "Very High"): "High",

    ("High", "Low"): "Moderate",
    ("High", "Moderate"): "High",
    ("High", "High"): "Severe",
    ("High", "Very High"): "Severe",

    ("Severe", "Low"): "High",
    ("Severe", "Moderate"): "Severe",
    ("Severe", "High"): "Severe",
    ("Severe", "Very High"): "Critical",
}

def fuse_risk(severity_level: str, probability_level: str) -> str:
    key = (severity_level, probability_level)
    if key not in RISK_MATRIX:
        raise ValueError(f"Invalid risk fusion input: {key}")
    return RISK_MATRIX[key]

# --------------------------------------------------
# Apply fusion
# --------------------------------------------------
df["risk_level"] = df.apply(
    lambda r: fuse_risk(r["severity_level"], r["probability_level"]),
    axis=1
)

# --------------------------------------------------
# Sanity checks
# --------------------------------------------------
print("\nFinal risk level distribution:")
print(df["risk_level"].value_counts())
print(df["risk_level"].value_counts(normalize=True))

# --------------------------------------------------
# Save output
# --------------------------------------------------
OUTPUT_PATH = DATA_DIR / "final_risk_output.csv"
df.to_csv(OUTPUT_PATH, index=False)

print("\nRisk fusion complete.")
print("Saved to:", OUTPUT_PATH)
print("PHASE 12.2 COMPLETE ✅")
