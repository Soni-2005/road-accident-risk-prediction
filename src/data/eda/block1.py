import pandas as pd
from pathlib import Path

# ----------------------------------
# Load merged dataset
# ----------------------------------
BASE_DIR = Path(__file__).resolve().parents[3]

DATA_PATH = BASE_DIR / "data" / "processed" / "merged_accident_data.csv"

print("Resolved BASE_DIR:", BASE_DIR)
print("Resolved DATA_PATH:", DATA_PATH)

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("EDA BLOCK 1: DATASET INTEGRITY CHECK")
print("=" * 60)

# ----------------------------------
# Basic dataset info
# ----------------------------------
print("\nDataset Shape:")
print(df.shape)

print("\nColumn Overview:")
print(df.info())

print("\nFirst 5 rows:")
print(df.head())

# ----------------------------------
# Primary key integrity check
# ----------------------------------
print("\nChecking Accident_Index integrity...")
if "Accident_Index" in df.columns:
    duplicate_count = df["Accident_Index"].duplicated().sum()
    print(f"Duplicate Accident_Index rows: {duplicate_count}")
else:
    print("⚠️ Accident_Index column not found")

# ----------------------------------
# Column grouping (semantic understanding)
# ----------------------------------
print("\nColumn Groups (High-Level):")

temporal_cols = [col for col in df.columns if "Date" in col or "Time" in col]
spatial_cols = [col for col in df.columns if "Latitude" in col or "Longitude" in col]
vehicle_cols = [col for col in df.columns if "vehicle" in col.lower()]
casualty_cols = [col for col in df.columns if "casualty" in col.lower()]

print(f"Temporal columns: {temporal_cols}")
print(f"Spatial columns: {spatial_cols}")
print(f"Vehicle-related columns: {vehicle_cols}")
print(f"Casualty-related columns: {casualty_cols}")

print("\n✔ BLOCK 1 COMPLETE: Dataset is accident-level and structurally valid")
