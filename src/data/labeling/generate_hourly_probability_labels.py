# src/data/labeling/generate_hourly_probability_labels.py

import pandas as pd
import numpy as np
from pathlib import Path

# -------------------------------------------------
# Configuration
# -------------------------------------------------
GRID_SIZE = 0.01  # ~1km grid
INPUT_PATH = Path("data/processed/merged_accident_data.csv")
OUTPUT_PATH = Path("data/processed/probability_labels_hourly.csv")

# -------------------------------------------------
# Main logic
# -------------------------------------------------
def main():
    print("=" * 70)
    print("PHASE 9.5 — HOURLY ACCIDENT PROBABILITY LABEL GENERATION (FIXED)")
    print("=" * 70)

    # -------------------------------------------------
    # Load data
    # -------------------------------------------------
    print("\n[1] Loading merged accident dataset...")
    df = pd.read_csv(INPUT_PATH, low_memory=False)

    required_cols = {"latitude", "longitude", "Time"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    print("Initial shape:", df.shape)

    # -------------------------------------------------
    # Spatial binning
    # -------------------------------------------------
    print("\n[2] Creating spatial grid bins...")
    df["lat_bin"] = np.floor(df["latitude"] / GRID_SIZE) * GRID_SIZE
    df["lon_bin"] = np.floor(df["longitude"] / GRID_SIZE) * GRID_SIZE

    # -------------------------------------------------
    # Hour extraction
    # -------------------------------------------------
    print("\n[3] Extracting hour from Time...")
    df["Hour"] = pd.to_datetime(df["Time"], errors="coerce").dt.hour

    before = len(df)
    df = df.dropna(subset=["Hour"])
    after = len(df)
    print(f"Dropped {before - after} rows with invalid time")

    df["Hour"] = df["Hour"].astype(int)

    # -------------------------------------------------
    # Accident counts per bin-hour
    # -------------------------------------------------
    print("\n[4] Counting accidents per (lat_bin, lon_bin, Hour)...")
    counts = (
        df.groupby(["lat_bin", "lon_bin", "Hour"])
          .size()
          .reset_index(name="accident_count")
    )

    # -------------------------------------------------
    # Construct FULL bin-hour space (Option A)
    # -------------------------------------------------
    print("\n[5] Constructing full bin-hour space (negatives included)...")

    unique_bins = counts[["lat_bin", "lon_bin"]].drop_duplicates()
    hours = pd.DataFrame({"Hour": range(24)})

    full_space = (
        unique_bins.assign(key=1)
        .merge(hours.assign(key=1), on="key")
        .drop(columns="key")
    )

    print("Total bin-hour combinations:", len(full_space))

    # -------------------------------------------------
    # Merge counts and assign labels
    # -------------------------------------------------
    print("\n[6] Merging accident counts and assigning labels...")
    labeled = full_space.merge(
        counts,
        on=["lat_bin", "lon_bin", "Hour"],
        how="left"
    )

    labeled["accident_count"] = labeled["accident_count"].fillna(0)
    labeled["accident_occurred"] = (labeled["accident_count"] >= 1).astype(int)

    labels = labeled[["lat_bin", "lon_bin", "Hour", "accident_occurred"]]

    # -------------------------------------------------
    # Save output
    # -------------------------------------------------
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    labels.to_csv(OUTPUT_PATH, index=False)

    print("\n✔ PHASE 9.5 COMPLETE (FIXED)")
    print("Output saved to:", OUTPUT_PATH)
    print("\nLabel distribution:")
    print(labels["accident_occurred"].value_counts())


if __name__ == "__main__":
    main()
