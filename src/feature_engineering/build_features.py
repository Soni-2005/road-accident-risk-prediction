import pandas as pd
from pathlib import Path

from src.feature_engineering.temporal_features import add_temporal_features
from src.feature_engineering.spatial_features import add_spatial_features
from src.feature_engineering.probability_features import compute_historical_accident_rate
from src.feature_engineering.severity_features import add_severity_features

# ----------------------------------
# Paths
# ----------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
SPLITS_DIR = BASE_DIR / "data" / "processed" / "splits"
OUT_DIR = BASE_DIR / "data" / "processed" / "features"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------------
# Load splits
# ----------------------------------
train = pd.read_csv(SPLITS_DIR / "train.csv", low_memory=False)
val = pd.read_csv(SPLITS_DIR / "val.csv", low_memory=False)
test = pd.read_csv(SPLITS_DIR / "test.csv", low_memory=False)

# ----------------------------------
# Shared features
# ----------------------------------
for name, df in [("train", train), ("val", val), ("test", test)]:
    df = add_temporal_features(df)
    df = add_spatial_features(df)

    if name == "train":
        train = df
    elif name == "val":
        val = df
    else:
        test = df

# ----------------------------------
# Probability features (TRAIN-only frequency)
# ----------------------------------
train["historical_accident_rate"] = compute_historical_accident_rate(train, train)
val["historical_accident_rate"] = compute_historical_accident_rate(train, val)
test["historical_accident_rate"] = compute_historical_accident_rate(train, test)

# ----------------------------------
# Severity features
# ----------------------------------
train = add_severity_features(train)
val = add_severity_features(val)
test = add_severity_features(test)

# ----------------------------------
# Save engineered datasets
# ----------------------------------
train.to_csv(OUT_DIR / "train_features.csv", index=False)
val.to_csv(OUT_DIR / "val_features.csv", index=False)
test.to_csv(OUT_DIR / "test_features.csv", index=False)

print("✔ PHASE 7 COMPLETE: Feature engineering artifacts saved")
print("Output directory:", OUT_DIR)
