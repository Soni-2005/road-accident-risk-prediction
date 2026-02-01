import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------------
# Resolve project root
# ----------------------------------
BASE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = BASE_DIR / "data" / "processed" / "merged_accident_data.csv"

print("=" * 70)
print("EDA BLOCK 5: FEATURE BEHAVIOR VS ACCIDENT SEVERITY")
print("=" * 70)

# ----------------------------------
# Load dataset
# ----------------------------------
df = pd.read_csv(DATA_PATH, low_memory=False)

# Keep only rows with valid severity
df = df.dropna(subset=["Accident_Severity"])

print("Dataset loaded for severity analysis:", df.shape)

# ----------------------------------
# 5.1 Severity vs Temporal Features
# ----------------------------------
print("\n[5.1] Severity vs Temporal Features")

df["Hour"] = pd.to_datetime(df["Time"], errors="coerce").dt.hour

severity_by_hour = (
    df.groupby("Hour")["Accident_Severity"]
    .mean()
)

print("\nAverage severity by hour:")
print(severity_by_hour)

plt.figure()
severity_by_hour.plot()
plt.title("Average Accident Severity by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Mean Severity")
plt.tight_layout()
plt.show()

# ----------------------------------
# 5.2 Severity vs Urban / Rural
# ----------------------------------
print("\n[5.2] Severity vs Urban/Rural")

if "Urban_or_Rural_Area" in df.columns:
    print(
        df.groupby("Urban_or_Rural_Area")["Accident_Severity"].mean()
    )

# ----------------------------------
# 5.3 Severity vs Road Characteristics
# ----------------------------------
print("\n[5.3] Severity vs Road Characteristics")

print("\nSeverity by Speed Limit:")
print(
    df.groupby("Speed_limit")["Accident_Severity"].mean()
)

plt.figure()
sns.boxplot(
    x="Speed_limit",
    y="Accident_Severity",
    data=df
)
plt.title("Severity vs Speed Limit")
plt.tight_layout()
plt.show()

# ----------------------------------
# 5.4 Severity vs Environmental Conditions
# ----------------------------------
print("\n[5.4] Severity vs Environmental Conditions")

print("\nSeverity by Light Conditions:")
print(
    df.groupby("Light_Conditions")["Accident_Severity"].mean()
)

print("\nSeverity by Weather Conditions:")
print(
    df.groupby("Weather_Conditions")["Accident_Severity"].mean()
)

# ----------------------------------
# 5.5 Severity vs Severity-Only Features
# ----------------------------------
print("\n[5.5] Severity vs Vehicle-related Features")

if "Number_of_Vehicles" in df.columns:
    print(
        df.groupby("Number_of_Vehicles")["Accident_Severity"].mean()
    )

if "avg_vehicle_age" in df.columns:
    print(
        df.groupby(pd.cut(df["avg_vehicle_age"], bins=5))["Accident_Severity"].mean()
    )

# ----------------------------------
# 5.6 Ambiguous Features Resolution
# ----------------------------------
print("\n[5.6] Ambiguous Feature Analysis")

ambiguous_features = [
    "Did_Police_Officer_Attend_Scene_of_Accident",
    "Carriageway_Hazards",
    "Special_Conditions_at_Site"
]

for col in ambiguous_features:
    if col in df.columns:
        print(f"\nSeverity by {col}:")
        print(
            df.groupby(col)["Accident_Severity"].mean()
        )

# ----------------------------------
# 5.7 Severity Class Separability Check
# ----------------------------------
print("\n[5.7] Severity Class Separability")

severity_counts = df["Accident_Severity"].value_counts(normalize=True)
print("\nSeverity class proportions:")
print(severity_counts)

print("""
Observations to note:
- Degree of overlap between severity levels
- Whether severity increases monotonically with key features
- Whether classes are meaningfully separable
""")

print("\n✔ BLOCK 5 COMPLETE: Severity behavior understood")
