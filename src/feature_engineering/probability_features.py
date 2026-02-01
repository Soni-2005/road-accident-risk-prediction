import pandas as pd

def compute_historical_accident_rate(
    train_df: pd.DataFrame,
    target_df: pd.DataFrame,
    group_cols=("location_id", "Hour", "Day_of_Week")
) -> pd.Series:
    """
    Computes normalized historical accident frequency using TRAIN data only.
    """
    freq = (
        train_df
        .groupby(list(group_cols))
        .size()
        .rename("accident_count")
        .reset_index()
    )

    # Normalize
    freq["historical_accident_rate"] = (
        freq["accident_count"] / freq["accident_count"].max()
    )

    merged = target_df.merge(
        freq[list(group_cols) + ["historical_accident_rate"]],
        on=list(group_cols),
        how="left"
    )

    return merged["historical_accident_rate"].fillna(0.0)
