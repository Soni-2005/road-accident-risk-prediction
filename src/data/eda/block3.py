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
print("EDA BLOCK 3: ACCIDENT PROBABILITY & FREQUENCY ANALYSIS")
print("=" * 70)

# ----------------------------------
# Load dataset
# ----------------------------------
df = pd.read_csv(DATA_PATH, low_memory=False)
print("Dataset loaded:", df.shape)

# ----------------------------------
# 3.1 Collapse to ACCIDENT-LEVEL view
# ----------------------------------
print("\n[3.1] Creating accident-level dataset...")

accident_cols = [
    "Accident_Index", "Date", "Time",
    "latitude", "longitude",
    "Day_of_Week", "Speed_limit",
    "Road_Type", "Junction_Detail",
    "Light_Conditions", "Weather_Conditions",
    "Road_Surface_Conditions",
    "Urban_or_Rural_Area"
]

df_acc = (
    df[accident_cols]
    .dropna(subset=["Accident_Index"])
    .drop_duplicates(subset="Accident_Index")
    .copy()
)

print("Accident-level shape:", df_acc.shape)
print("Unique accidents:", df_acc["Accident_Index"].nunique())

# ----------------------------------
# 3.2 Temporal frequency analysis
# ----------------------------------
print("\n[3.2] Temporal frequency analysis")

# Convert Date & Time
df_acc["Date"] = pd.to_datetime(df_acc["Date"], errors="coerce")
df_acc["Hour"] = pd.to_datetime(df_acc["Time"], errors="coerce").dt.hour
df_acc["Month"] = df_acc["Date"].dt.month

# Accidents by hour
hourly_counts = df_acc["Hour"].value_counts().sort_index()
print("\nAccidents by Hour:")
print(hourly_counts)

plt.figure()
sns.lineplot(x=hourly_counts.index, y=hourly_counts.values)
plt.title("Accident Frequency by Hour of Day")
plt.xlabel("Hour")
plt.ylabel("Number of Accidents")
plt.show()

# Accidents by day of week
dow_counts = df_acc["Day_of_Week"].value_counts().sort_index()
print("\nAccidents by Day of Week:")
print(dow_counts)

# ----------------------------------
# 3.3 Spatial frequency analysis
# ----------------------------------
print("\n[3.3] Spatial frequency analysis")

# Bin lat-long to detect clusters (coarse)
df_acc["lat_bin"] = df_acc["latitude"].round(2)
df_acc["lon_bin"] = df_acc["longitude"].round(2)

spatial_freq = (
    df_acc.groupby(["lat_bin", "lon_bin"])
    .size()
    .reset_index(name="accident_count")
    .sort_values("accident_count", ascending=False)
)

print("\nTop high-frequency accident zones:")
print(spatial_freq.head(10))

# ----------------------------------
# 3.4 Context-based frequency
# ----------------------------------
print("\n[3.4] Context-based accident frequency")

speed_freq = df_acc["Speed_limit"].value_counts().sort_index()
print("\nAccidents by Speed Limit:")
print(speed_freq)

weather_freq = df_acc["Weather_Conditions"].value_counts().sort_index()
print("\nAccidents by Weather Condition:")
print(weather_freq)

light_freq = df_acc["Light_Conditions"].value_counts().sort_index()
print("\nAccidents by Light Condition:")
print(light_freq)

# ----------------------------------
# 3.5 Repeated accidents at same locations
# ----------------------------------
print("\n[3.5] Repeated accidents at same locations")

repeat_locations = spatial_freq[spatial_freq["accident_count"] > 5]
print(
    f"Locations with more than 5 accidents: {repeat_locations.shape[0]}"
)

# ----------------------------------
# 3.6 Probability proxy definition (conceptual)
# ----------------------------------
print("\n[3.6] Probability Proxy Design")

print("""
Accident Probability Proxy (to be used later):

- Based on normalized accident frequency
- Computed over:
  (location bin × time window × road context)

Higher historical frequency ⇒ higher accident probability
""")

print("\n✔ BLOCK 3 COMPLETE: Probability modeling foundation established")
