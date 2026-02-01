import pandas as pd

def add_spatial_features(df: pd.DataFrame, bin_size: float = 0.02) -> pd.DataFrame:
    out = df.copy()

    out["lat_bin"] = (out["latitude"] / bin_size).round(0) * bin_size
    out["lon_bin"] = (out["longitude"] / bin_size).round(0) * bin_size

    # Combined location id
    out["location_id"] = out["lat_bin"].astype(str) + "_" + out["lon_bin"].astype(str)

    return out
