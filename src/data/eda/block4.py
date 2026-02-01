import pandas as pd
from pathlib import Path

# ----------------------------------
# Resolve project root
# ----------------------------------
BASE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = BASE_DIR / "data" / "processed" / "merged_accident_data.csv"

print("=" * 70)
print("EDA BLOCK 4: FEATURE AVAILABILITY & LEAKAGE CHECK")
print("=" * 70)

# ----------------------------------
# Load dataset
# ----------------------------------
df = pd.read_csv(DATA_PATH, low_memory=False)
print("Dataset loaded:", df.shape)

# ----------------------------------
# Define feature buckets
# ----------------------------------

probability_safe_features = [
    # Temporal
    "Date", "Time", "Day_of_Week",
    
    # Spatial
    "latitude", "longitude",
    "Local_Authority_(District)", "LSOA_of_Accident_Location",
    
    # Road & environment
    "Road_Type", "Speed_limit",
    "Junction_Detail", "Junction_Control",
    "Light_Conditions", "Weather_Conditions",
    "Road_Surface_Conditions",
    "Urban_or_Rural_Area"
]

severity_only_features = [
    "Number_of_Vehicles",
    "avg_vehicle_age",
    "most_common_vehicle_type"
]

leakage_features = [
    "Accident_Severity",
    "Number_of_Casualties",
    "total_casualties",
    "fatal_casualties",
    "serious_casualties",
    "slight_casualties"
]

ambiguous_features = [
    "Police_Force",
    "Did_Police_Officer_Attend_Scene_of_Accident",
    "Special_Conditions_at_Site",
    "Carriageway_Hazards",
    "Pedestrian_Crossing-Human_Control",
    "Pedestrian_Crossing-Physical_Facilities"
]

# ----------------------------------
# Validate feature presence
# ----------------------------------
all_features = set(df.columns)

def present(features):
    return [f for f in features if f in all_features]

# ----------------------------------
# Print categorized features
# ----------------------------------
print("\n[Probability-Safe Features]")
print(present(probability_safe_features))

print("\n[Severity-Only Features]")
print(present(severity_only_features))

print("\n[Leakage / Outcome Features]")
print(present(leakage_features))

print("\n[Ambiguous / Review Required Features]")
print(present(ambiguous_features))

# ----------------------------------
# Features not yet classified
# ----------------------------------
classified = set(
    present(probability_safe_features)
    + present(severity_only_features)
    + present(leakage_features)
    + present(ambiguous_features)
)

unclassified = sorted(list(all_features - classified))

print("\n[Unclassified Features]")
print(unclassified)

print("\n✔ BLOCK 4 COMPLETE: Feature governance established")
