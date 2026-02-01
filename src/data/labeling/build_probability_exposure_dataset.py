# src/data/labeling/build_probability_exposure_dataset.py

import pandas as pd
import numpy as np
from pathlib import Path

# -------------------------------------------------
# Configuration
# -------------------------------------------------
GRID_SIZE = 0.01
MERGED_PATH = Path("data/processed/merged_accident_data.csv")
LABELS_PATH = Path("data/processed/probability_labels_hourly.csv")
OUTPUT_PATH = Path("data/processed/probability_exposure_dataset.csv")

# -------------------------------------------------
# Helpers
# -------------------------------------------------
def spatial_bin(series):
    return np.floor(series / GRID_SIZE) * GRID_SIZE

# -------------------------------------------------
# Main
# -------------------------------------------------
def main():
    print("=" * 72)
    print("PHASE 9.6 — PROBABILITY EXPOSURE DATASET CONSTRUCTION")
    print("=" * 72)

    # -------------------------------------------------
    # Load data
    # -------------------------------------------------
    print("\n[1] Loading merged accident data...")
    df = pd.read_csv(MERGED_PATH, low_memory=False)

    print("[2] Loading hourly probability labels...")
    labels = pd.read_csv(LABELS_PATH)

    # -------------------------------------------------
    # Create spatial bins (for aggregation only)
    # -------------------------------------------------
    print("\n[3] Creating spatial bins...")
    df["lat_bin"] = spatial_bin(df["latitude"])
    df["lon_bin"] = spatial_bin(df["longitude"])

    # -------------------------------------------------
    # Aggregate STATIC / CONTEXT features per spatial bin
    # -------------------------------------------------
    print("\n[4] Aggregating static context features per spatial bin...")

    agg_spec = {
        "Speed_limit": "mean",
        "Road_Type": lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan,
        "Junction_Detail": lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan,
        "Urban_or_Rural_Area": lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan,
        "Light_Conditions": lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan,
        "Weather_Conditions": lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan,
    }

    context = (
        df.groupby(["lat_bin", "lon_bin"], as_index=False)
          .agg(agg_spec)
    )

    print("Context feature shape:", context.shape)

    # -------------------------------------------------
    # Join context with hourly exposure labels
    # -------------------------------------------------
    print("\n[5] Joining context features with exposure labels...")
    exposure = labels.merge(
        context,
        on=["lat_bin", "lon_bin"],
        how="left"
    )

    # -------------------------------------------------
    # Temporal exposure-safe features
    # -------------------------------------------------
    print("\n[6] Creating temporal exposure features...")
    exposure["is_peak_hour"] = exposure["Hour"].isin([7, 8, 9, 16, 17, 18]).astype(int)
    exposure["is_night"] = exposure["Hour"].isin([0, 1, 2, 3, 4, 22, 23]).astype(int)

    # -------------------------------------------------
    # Final cleanup
    # -------------------------------------------------
    print("\n[7] Final cleanup and validation...")

    # Drop rows with missing context (rare bins)
    before = len(exposure)
    exposure = exposure.dropna()
    after = len(exposure)
    print(f"Dropped {before - after} rows with missing context")

    # Ensure target exists
    assert "accident_occurred" in exposure.columns

    # -------------------------------------------------
    # Save output
    # -------------------------------------------------
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    exposure.to_csv(OUTPUT_PATH, index=False)

    print("\n✔ PHASE 9.6 COMPLETE")
    print("Output saved to:", OUTPUT_PATH)
    print("Final shape:", exposure.shape)
    print("\nTarget distribution:")
    print(exposure["accident_occurred"].value_counts(normalize=True))


if __name__ == "__main__":
    main()
