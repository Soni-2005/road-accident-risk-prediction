import pandas as pd

def add_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    out["Date"] = pd.to_datetime(out["Date"], errors="coerce")
    out["Hour"] = pd.to_datetime(out["Time"], errors="coerce").dt.hour

    out["month"] = out["Date"].dt.month
    out["is_weekend"] = out["Day_of_Week"].isin([6, 7]).astype(int)

    # Peak hours: 8–10 AM, 4–7 PM
    out["is_peak_hour"] = out["Hour"].isin([8, 9, 10, 16, 17, 18, 19]).astype(int)

    # Night: 9 PM–5 AM
    out["is_night"] = out["Hour"].isin([21, 22, 23, 0, 1, 2, 3, 4, 5]).astype(int)

    return out
