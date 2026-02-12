import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ==================================================
# STEP 11.3b — SEVERITY SCORE ANALYSIS (FINAL)
# ==================================================

# --------------------------------------------------
# Resolve project root
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[3]

DATA_PATH = BASE_DIR / "data" / "processed" / "sev_val_scored.csv"
REPORT_DIR = BASE_DIR / "reports" / "severity"
PLOT_DIR = REPORT_DIR / "plots"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
PLOT_DIR.mkdir(parents=True, exist_ok=True)

TARGET_COL = "Accident_Severity"
SCORE_COL = "severity_score"

# --------------------------------------------------
# Load data
# --------------------------------------------------
print("Loading scored validation dataset...")
df = pd.read_csv(DATA_PATH)
print("Shape:", df.shape)

# --------------------------------------------------
# 🔑 Robust label detection
# --------------------------------------------------
unique_labels = sorted(df[TARGET_COL].unique())

print("Detected severity labels:", unique_labels)

if len(unique_labels) < 2:
    raise ValueError("Severity analysis requires at least 2 classes")

slight_label = unique_labels[0]
serious_label = unique_labels[-1]

print(f"Interpreting label {slight_label} as SLIGHT")
print(f"Interpreting label {serious_label} as SERIOUS")

print(df["Accident_Severity"].value_counts())
print(df["Accident_Severity"].value_counts(normalize=True))

df_slight = df[df[TARGET_COL] == 1]
df_serious = df[df[TARGET_COL] >= 2]

print("Severity grouping used:")
print("SLIGHT  → Accident_Severity == 1")
print("SERIOUS → Accident_Severity >= 2")

print(f"Slight cases : {len(df_slight)}")
print(f"Serious cases: {len(df_serious)}")

# --------------------------------------------------
# 1️⃣ Overall severity score distribution
# --------------------------------------------------
plt.figure()
plt.hist(df[SCORE_COL], bins=50)
plt.title("Overall Severity Score Distribution")
plt.xlabel("Severity Score (P(Serious))")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(PLOT_DIR / "severity_score_overall.png")
plt.close()

# --------------------------------------------------
# 2️⃣ Class-conditional distributions
# --------------------------------------------------
plt.figure()
plt.hist(df_slight[SCORE_COL], bins=50, alpha=0.7, label="Slight")
plt.hist(df_serious[SCORE_COL], bins=50, alpha=0.7, label="Serious")
plt.title("Severity Score by True Class")
plt.xlabel("Severity Score (P(Serious))")
plt.ylabel("Count")
plt.legend()
plt.tight_layout()
plt.savefig(PLOT_DIR / "severity_score_by_class.png")
plt.close()

# --------------------------------------------------
# 3️⃣ Summary statistics
# --------------------------------------------------
summary = pd.DataFrame({
    "Class": ["Slight", "Serious"],
    "Count": [len(df_slight), len(df_serious)],
    "Mean": [
        df_slight[SCORE_COL].mean(),
        df_serious[SCORE_COL].mean()
    ],
    "Median": [
        df_slight[SCORE_COL].median(),
        df_serious[SCORE_COL].median()
    ],
    "25th Percentile": [
        df_slight[SCORE_COL].quantile(0.25),
        df_serious[SCORE_COL].quantile(0.25)
    ],
    "75th Percentile": [
        df_slight[SCORE_COL].quantile(0.75),
        df_serious[SCORE_COL].quantile(0.75)
    ]
})

# --------------------------------------------------
# 4️⃣ False-negative risk zone inspection
# --------------------------------------------------
LOW_SCORE_THRESHOLD = 0.30
low_score_serious = df_serious[df_serious[SCORE_COL] < LOW_SCORE_THRESHOLD]

# --------------------------------------------------
# Save analysis report
# --------------------------------------------------
report_path = REPORT_DIR / "severity_score_analysis.txt"

with open(report_path, "w") as f:
    f.write("SEVERITY SCORE ANALYSIS — STEP 11.3b\n")
    f.write("=" * 50 + "\n\n")

    f.write("Label Interpretation\n")
    f.write(f"Slight label  : {slight_label}\n")
    f.write(f"Serious label : {serious_label}\n\n")

    f.write("Dataset Summary\n")
    f.write(f"Total samples : {len(df)}\n")
    f.write(f"Slight cases  : {len(df_slight)}\n")
    f.write(f"Serious cases : {len(df_serious)}\n\n")

    f.write("Severity Score Summary Statistics\n")
    f.write(summary.to_string(index=False))
    f.write("\n\n")

    f.write("False-Negative Risk Zone Analysis\n")
    f.write(f"Threshold: severity_score < {LOW_SCORE_THRESHOLD}\n")
    f.write(f"Serious cases below threshold: {len(low_score_serious)}\n")
    f.write(
        f"Percentage of serious cases: "
        f"{(len(low_score_serious) / len(df_serious)) * 100:.2f}%\n"
    )

print("\nSeverity score analysis complete.")
print("Plots saved to:", PLOT_DIR)
print("Report saved to:", report_path)

print("\nSTEP 11.3b COMPLETE ✅")
