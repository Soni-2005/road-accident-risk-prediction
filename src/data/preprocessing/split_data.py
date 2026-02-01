import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

# ----------------------------------
# Resolve project root
# ----------------------------------
BASE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = BASE_DIR / "data" / "processed" / "merged_accident_data.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed" / "splits"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Resolved BASE_DIR:", BASE_DIR)
print("Resolved DATA_PATH:", DATA_PATH)

df = pd.read_csv(DATA_PATH, low_memory=False)

# Keep only valid severity rows
df = df.dropna(subset=["Accident_Severity"])

print("Dataset shape after filtering:", df.shape)

# ----------------------------------
# First split: Train (70%) vs Temp (30%)
# ----------------------------------
train_df, temp_df = train_test_split(
    df,
    test_size=0.30,
    random_state=42,
    stratify=df["Accident_Severity"]
)

# ----------------------------------
# Second split: Validation (15%) vs Test (15%)
# ----------------------------------
val_df, test_df = train_test_split(
    temp_df,
    test_size=0.50,
    random_state=42,
    stratify=temp_df["Accident_Severity"]
)

print("Train shape:", train_df.shape)
print("Validation shape:", val_df.shape)
print("Test shape:", test_df.shape)

# ----------------------------------
# Save splits
# ----------------------------------
train_df.to_csv(OUTPUT_DIR / "train.csv", index=False)
val_df.to_csv(OUTPUT_DIR / "val.csv", index=False)
test_df.to_csv(OUTPUT_DIR / "test.csv", index=False)

print("\n✔ Data splits saved to:", OUTPUT_DIR)
