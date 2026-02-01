import pandas as pd

def add_severity_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # Vehicle interaction features
    out["multi_vehicle_flag"] = (out["Number_of_Vehicles"] > 1).astype(int)

    out["old_vehicle_flag"] = (out["avg_vehicle_age"] >= 15).astype(int)

    # Environmental interaction features
    out["speed_x_light"] = out["Speed_limit"] * out["Light_Conditions"]
    out["speed_x_weather"] = out["Speed_limit"] * out["Weather_Conditions"]

    # Ambiguous features resolved as flags
    if "Carriageway_Hazards" in out.columns:
        out["hazard_present"] = (out["Carriageway_Hazards"] > 0).astype(int)

    if "Special_Conditions_at_Site" in out.columns:
        out["special_site_flag"] = (out["Special_Conditions_at_Site"] > 0).astype(int)

    return out
