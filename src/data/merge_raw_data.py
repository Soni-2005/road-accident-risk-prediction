import pandas as pd
from pathlib import Path

# -------------------------------
# Paths
# -------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

print("Base dir:", BASE_DIR)
print("Raw dir:", RAW_DIR)

# -------------------------------
# Load raw datasets
# -------------------------------
accidents = pd.read_csv(RAW_DIR / "AccidentsBig.csv")
vehicles = pd.read_csv(RAW_DIR / "VehiclesBig.csv")
casualties = pd.read_csv(RAW_DIR / "CasualtiesBig.csv")

print("Files loaded successfully")
print(f"Accidents: {accidents.shape}")
print(f"Vehicles: {vehicles.shape}")
print(f"Casualties: {casualties.shape}")

# -------------------------------
# Aggregate VEHICLES data
# -------------------------------
vehicles_agg = (
    vehicles
    .groupby("Accident_Index")
    .agg(
        total_vehicles=("Vehicle_Reference", "count"),
        avg_vehicle_age=("Age_of_Vehicle", "mean"),
        most_common_vehicle_type=("Vehicle_Type", lambda x: x.mode().iloc[0] if not x.mode().empty else -1)
    )
    .reset_index()
)

print("Vehicles aggregated")

# -------------------------------
# Aggregate CASUALTIES data
# -------------------------------
casualties_agg = (
    casualties
    .groupby("Accident_Index")
    .agg(
        total_casualties=("Casualty_Reference", "count"),
        fatal_casualties=("Casualty_Severity", lambda x: (x == 1).sum()),
        serious_casualties=("Casualty_Severity", lambda x: (x == 2).sum()),
        slight_casualties=("Casualty_Severity", lambda x: (x == 3).sum())
    )
    .reset_index()
)

print("Casualties aggregated")

# -------------------------------
# Merge everything with ACCIDENTS
# -------------------------------
merged_df = accidents.merge(
    vehicles_agg,
    on="Accident_Index",
    how="left"
).merge(
    casualties_agg,
    on="Accident_Index",
    how="left"
)

print("Datasets merged successfully")

# -------------------------------
# Handle missing aggregated values
# -------------------------------
merged_df.fillna({
    "total_vehicles": 0,
    "total_casualties": 0,
    "fatal_casualties": 0,
    "serious_casualties": 0,
    "slight_casualties": 0
}, inplace=True)

# -------------------------------
# Save processed dataset
# -------------------------------
output_path = PROCESSED_DIR / "merged_accident_data.csv"
merged_df.to_csv(output_path, index=False)

print(f"Final merged dataset saved at: {output_path}")
print(f"Final shape: {merged_df.shape}")
