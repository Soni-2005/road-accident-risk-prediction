import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------------
# Resolve project root correctly
# ----------------------------------
BASE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = BASE_DIR / "data" / "processed" / "merged_accident_data.csv"

print("=" * 60)
print("EDA BLOCK 2: ACCIDENT SEVERITY ANALYSIS")
print("=" * 60)

# ----------------------------------
# Load dataset
# ----------------------------------
df = pd.read_csv(DATA_PATH)
print("Dataset loaded successfully")
print("Shape:", df.shape)

# ----------------------------------
# Check target availability
# ----------------------------------
if "Accident_Severity" not in df.columns:
    raise ValueError("❌ Accident_Severity column not found in dataset")

# ----------------------------------
# Severity distribution
# ----------------------------------
severity_counts = df["Accident_Severity"].value_counts().sort_index()
severity_percent = round(severity_counts / severity_counts.sum() * 100, 2)

severity_df = pd.DataFrame({
    "Count": severity_counts,
    "Percentage (%)": severity_percent
})

print("\nAccident Severity Distribution:")
print(severity_df)

# ----------------------------------
# Visualization
# ----------------------------------
plt.figure()
sns.countplot(
    x="Accident_Severity",
    data=df
)
plt.title("Accident Severity Distribution")
plt.xlabel("Severity Level")
plt.ylabel("Number of Accidents")
plt.tight_layout()
plt.show()

# ----------------------------------
# Severity vs casualties sanity check
# ----------------------------------
if "total_casualties" in df.columns:
    print("\nAverage casualties per severity level:")
    print(
        df.groupby("Accident_Severity")["total_casualties"].mean()
    )

print("\n✔ BLOCK 2 COMPLETE: Severity target understood")
